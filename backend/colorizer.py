from astropy.io import fits
from astropy.visualization import make_lupton_rgb, AsinhStretch, SqrtStretch, LinearStretch
import numpy as np
from PIL import Image

def get_stretch_function(stretch_name='asinh'):
    """Selects the stretch function based on name."""
    if stretch_name == 'sqrt':
        return SqrtStretch()
    if stretch_name == 'linear':
        return LinearStretch()
    # Default to AsinhStretch, which is great for astronomical images
    return AsinhStretch()

def colorize_fits(fits_data, red_channel, green_channel, blue_channel, stretch_name='asinh', q=8, minimum=0):
    """
    Colorizes a FITS data cube by mapping specified channels to RGB.
    This function represents the core logic of Processes 0.2.1, 0.2.2, and 0.2.3.

    Args:
        fits_data (numpy.ndarray): The data from the FITS file (a 3D cube).
        red_channel (int): Index of the data layer for the Red channel.
        green_channel (int): Index of the data layer for the Green channel.
        blue_channel (int): Index of the data layer for the Blue channel.
        stretch_name (str): The name of the stretch function ('asinh', 'sqrt', 'linear').
        q (float): The asinh softening parameter, controls the stretch intensity.
        minimum (float): The minimum intensity value to map to black.

    Returns:
        PIL.Image: The colorized RGB image object.
    """
    # Ensure we have a 3D data cube (multiple images)
    if fits_data.ndim != 3 or fits_data.shape[0] < max(red_channel, green_channel, blue_channel) + 1:
        raise ValueError("Input FITS data must be a 3D cube with enough channels for the selected mapping.")

    # Assign the data layers to R, G, B channels
    image_r = fits_data[red_channel, :, :]
    image_g = fits_data[green_channel, :, :]
    image_b = fits_data[blue_channel, :, :]

    stretch = get_stretch_function(stretch_name)

    # Use a standard astronomical library function to create a visually appealing RGB image
    rgb_image = make_lupton_rgb(image_r, image_g, image_b, minimum=minimum, stretch=stretch, Q=q)

    # Convert the resulting numpy array to a PIL Image for easy saving and serving
    pil_image = Image.fromarray(rgb_image)
    return pil_image