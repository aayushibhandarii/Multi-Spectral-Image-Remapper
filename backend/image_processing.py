from PIL import Image
import numpy as np
from models import ProcessedImage
from denoiser import AstronomicalDenoiser

class AIModel:
    """AI Model Engine with proper RGB processing based on reference code."""
    
    def get_prediction(self, fits_data, model_params):
        """This is where the 'AI' colorization happens."""
        return self._colorize(fits_data, 
                              red_channel=model_params['red_channel'],
                              green_channel=model_params['green_channel'],
                              blue_channel=model_params['blue_channel'],
                              stretch_name=model_params['stretch_name'],
                              power=model_params['power'],
                              black_point=model_params['black_point'],
                              white_point=model_params['white_point'],
                              saturation=model_params['saturation'],
                              red_scale=model_params['red_scale'],
                              green_scale=model_params['green_scale'],
                              blue_scale=model_params['blue_scale'])

    def _stretch_data(self, data, method='power', power=2.4, black_point=0.5, white_point=99.8):
        """Apply stretch method to data based on reference code."""
        # Ensure float32 for efficiency
        data = data.astype(np.float32)
        
        # Handle NaN and inf values
        data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Clip background and foreground using percentiles
        vmin = np.percentile(data, black_point)
        vmax = np.percentile(data, white_point)
        
        # Normalize to 0-1 range
        data = (data - vmin) / (vmax - vmin + 1e-10)
        data = np.clip(data, 0, 1)
        
        # Apply stretch method
        if method == 'power':
            data = np.power(data, 1.0 / power)
        elif method == 'asinh':
            asinh_scale = 0.05
            data = np.arcsinh(data / asinh_scale) / np.arcsinh(1.0 / asinh_scale)
            data = (data - data.min()) / (data.max() - data.min() + 1e-10)
        elif method == 'sqrt':
            data = np.sqrt(data)
        elif method == 'log':
            data = np.log1p(data * 10) / np.log1p(10)
        
        return data

    def _boost_saturation_hsv(self, rgb, factor):
        """Boost color saturation using HSV color space."""
        if factor == 1.0:
            return rgb
        
        # Convert RGB to HSV
        # RGB assumed to be in range [0, 1]
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        
        maxc = np.maximum(np.maximum(r, g), b)
        minc = np.minimum(np.minimum(r, g), b)
        v = maxc
        
        deltac = maxc - minc
        s = deltac / (maxc + 1e-10)
        deltac = np.where(deltac == 0, 1, deltac)  # Avoid division by zero
        
        rc = (maxc - r) / deltac
        gc = (maxc - g) / deltac
        bc = (maxc - b) / deltac
        
        h = np.zeros_like(v)
        h = np.where(r == maxc, bc - gc, h)
        h = np.where(g == maxc, 2.0 + rc - bc, h)
        h = np.where(b == maxc, 4.0 + gc - rc, h)
        h = (h / 6.0) % 1.0
        
        # Boost saturation
        s = np.clip(s * factor, 0, 1)
        
        # Convert back to RGB
        i = (h * 6.0).astype(int)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        conditions = [
            i == 0, i == 1, i == 2, i == 3, i == 4, i == 5
        ]
        
        r = np.select(conditions, [v, q, p, p, t, v])
        g = np.select(conditions, [t, v, v, q, p, p])
        b = np.select(conditions, [p, p, t, v, v, q])
        
        return np.dstack([r, g, b])

    def _colorize(self, fits_data, red_channel, green_channel, blue_channel, 
                  stretch_name, power, black_point, white_point, saturation,
                  red_scale, green_scale, blue_scale):
        """Create RGB image with proper stretching based on reference code."""
        
        if fits_data.ndim != 3 or fits_data.shape[0] < max(red_channel, green_channel, blue_channel) + 1:
            raise ValueError("Input FITS data must be a 3D cube with enough channels.")

        # Extract channels
        image_r = fits_data[red_channel, :, :].astype(np.float32)
        image_g = fits_data[green_channel, :, :].astype(np.float32)
        image_b = fits_data[blue_channel, :, :].astype(np.float32)

        # Apply color balance multipliers
        if red_scale != 1.0:
            image_r = image_r * red_scale
        if green_scale != 1.0:
            image_g = image_g * green_scale
        if blue_scale != 1.0:
            image_b = image_b * blue_scale

        # Stretch each channel individually
        stretched_r = self._stretch_data(image_r, stretch_name, power, black_point, white_point)
        stretched_g = self._stretch_data(image_g, stretch_name, power, black_point, white_point)
        stretched_b = self._stretch_data(image_b, stretch_name, power, black_point, white_point)

        # Stack into RGB (range 0-1)
        rgb = np.dstack([stretched_r, stretched_g, stretched_b])

        # Apply saturation boost
        if saturation != 1.0:
            rgb = self._boost_saturation_hsv(rgb, saturation)

        # Convert to 8-bit (0-255)
        rgb = np.clip(rgb * 255, 0, 255).astype(np.uint8)
        
        return Image.fromarray(rgb, mode='RGB')


class ImageProcessor:
    """Handles the core image processing workflow with ML denoising."""
    def __init__(self):
        self.model_engine = AIModel()
        # Initialize ML denoiser
        self.denoiser = AstronomicalDenoiser(model_path='models/dncnn_astro.pth')

    def process_image(self, fits_data, model_params):
        """Orchestrates the colorization from FITS data to a ProcessedImage."""
        
        # Get raw FITS data
        raw_data = fits_data.get_raw_data()
        
        # Apply ML denoising if enabled
        if model_params.get('use_denoising', True):  # Default to True
            print("🤖 Applying ML-based noise reduction...")
            denoised_data = self.denoiser.denoise_fits_cube(raw_data)
            print("✓ Denoising complete!")
        else:
            print("⊗ Denoising disabled, using raw data")
            denoised_data = raw_data
        
        # Colorize the (denoised) data
        pil_image = self.model_engine.get_prediction(denoised_data, model_params)
        
        return ProcessedImage(pil_image)