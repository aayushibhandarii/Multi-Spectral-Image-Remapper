import os
import numpy as np
from astropy.io import fits
from image_processing import ImageProcessor
from history_manager import HistoryManager
from models import FITSData, HistoryItem
import base64
from io import BytesIO
from datetime import datetime

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

# These configurations represent the "AI Models and Palettes"
MODELS = {
  'hubble': { 'name': 'Hubble Palette (SHO)', 'red_channel': 2, 'green_channel': 1, 'blue_channel': 0 },
  'natural': { 'name': 'Natural Color (RGB)', 'red_channel': 0, 'green_channel': 1, 'blue_channel': 2 },
  'custom': { 
    'red_channel': 0,   # I filter → Red channel
    'green_channel': 1, # V filter → Green channel  
    'blue_channel': 2,  # B filter → Blue channel
    'stretch_name': 'asinh',
    'power': 3.0,
    'black_point': 1.0,
    'white_point': 99.5,
    'saturation': 1.5,
    'red_scale': 1.2,
    'green_scale': 1.0,
    'blue_scale': 0.9
}
}

class AppController:
    """The central coordinator for the application."""
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.history_manager = HistoryManager()
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(STATIC_FOLDER, exist_ok=True)

    def colorize_layers(self, files, model_params):
        """Handles the full colorization process for separate layer files."""
        try:
            # Save the files first
            filenames = {}
            for channel, file_storage in files.items():
                filepath = os.path.join(UPLOAD_FOLDER, file_storage.filename)
                file_storage.save(filepath)
                filenames[channel] = file_storage.filename

            # Load each file and stack them into a data cube
            r_path = os.path.join(UPLOAD_FOLDER, filenames['red'])
            g_path = os.path.join(UPLOAD_FOLDER, filenames['green'])
            b_path = os.path.join(UPLOAD_FOLDER, filenames['blue'])

            with fits.open(r_path) as hdul_r, fits.open(g_path) as hdul_g, fits.open(b_path) as hdul_b:
                data_r = hdul_r[0].data
                data_g = hdul_g[0].data
                data_b = hdul_b[0].data

                # Downsample the data to reduce memory usage
                downsample_factor = 4
                data_r = data_r[::downsample_factor, ::downsample_factor]
                data_g = data_g[::downsample_factor, ::downsample_factor]
                data_b = data_b[::downsample_factor, ::downsample_factor]

                stacked_data = np.stack([data_r, data_g, data_b])
                fits_data_obj = FITSData(data=stacked_data, header=hdul_r[0].header)
            
            input_filename_for_history = f"{filenames['red']}, {filenames['green']}, {filenames['blue']}"
            
            # Get palette from frontend, or default to 'natural'
            selected_palette = model_params.get('palette', 'natural')
            palette_config = MODELS.get(selected_palette, MODELS['natural'])

            # Set channel mappings based on selected palette
            model_params['red_channel'] = palette_config['red_channel']
            model_params['green_channel'] = palette_config['green_channel']
            model_params['blue_channel'] = palette_config['blue_channel']

            # Enhanced stretch parameters based on reference code
            model_params['stretch_name'] = model_params.get('stretch_name', 'power')
            model_params['power'] = model_params.get('power', 2.4)
            model_params['black_point'] = model_params.get('black_point', 0.5)
            model_params['white_point'] = model_params.get('white_point', 99.8)
            model_params['saturation'] = model_params.get('saturation', 1.3)
            model_params['red_scale'] = model_params.get('red_scale', 1.0)
            model_params['green_scale'] = model_params.get('green_scale', 1.0)
            model_params['blue_scale'] = model_params.get('blue_scale', 1.0)
            
            # ML Denoising parameter (new!)
            model_params['use_denoising'] = model_params.get('use_denoising', True)

            # Process image with ML denoising
            processed_image = self.image_processor.process_image(fits_data_obj, model_params)
            
            pil_img = processed_image.export_to()

            # Encode image to Base64
            buffered = BytesIO()
            pil_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_data = f"data:image/png;base64,{img_str}"

            self.history_manager.add_entry(HistoryItem(
                input_filename=input_filename_for_history,
                settings_used=model_params,
                status="Success"
            ))

            serializable_metadata = {k: str(v) for k, v in fits_data_obj.header.items()}

            return {"imageData": image_data, "metadata": serializable_metadata}, None

        except Exception as e:
            self.history_manager.add_entry(HistoryItem(
                input_filename=str(filenames),
                settings_used=model_params,
                status="Failure"
            ))
            return None, str(e)

    def get_history(self):
        return self.history_manager.get_history()