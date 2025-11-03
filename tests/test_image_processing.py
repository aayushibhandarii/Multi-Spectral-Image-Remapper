
import os
import pytest
import numpy as np
from PIL import Image
from astropy.io import fits

from backend.image_processing import ImageProcessor
from backend.models import FITSData # Assuming FITSData is in models.py

# --- IMPORTANT --- #
# Change this to the name of a FITS file in your `backend/uploads` folder.
# The test will fail if this file does not exist.
TEST_FITS_FILE_NAME = "sample.fits" # <--- CHANGE THIS IF NEEDED

@pytest.fixture
def image_processor():
    """Provides an instance of the ImageProcessor."""
    return ImageProcessor()

@pytest.fixture
def fits_data():
    """
    Provides FITS data for testing. Skips the test if the file is not found.
    """
    file_path = os.path.join("backend", "uploads", TEST_FITS_FILE_NAME)
    if not os.path.exists(file_path):
        pytest.skip(f"Test file not found at {file_path}. Please place a FITS file there.")
    
    with fits.open(file_path) as hdul:
        data_cube = hdul[0].data
        header = hdul[0].header
    
    # Ensure data is a 3D cube for color processing
    if data_cube.ndim == 2:
        # If 2D, stack it to make a 3-channel grayscale image for testing
        data_cube = np.stack([data_cube] * 3, axis=0)
        
    return FITSData(header_data=dict(header), data_cube=data_cube)

def test_process_image(image_processor, fits_data):
    """
    Tests the full image processing workflow.
    Input: A FITSData object containing data from a real FITS file.
    Output: A ProcessedImage object containing a PIL Image.
    """
    # These are example parameters. Adjust them as needed.
    model_params = {
        'red_channel': 0,
        'green_channel': 1,
        'blue_channel': 2,
        'stretch_name': 'power',
        'power': 2.4,
        'black_point': 0.5,
        'white_point': 99.8,
        'saturation': 1.5,
        'red_scale': 1.0,
        'green_scale': 1.0,
        'blue_scale': 1.0,
    }

    # Process the image
    processed_image_obj = image_processor.process_image(fits_data, model_params)

    # Verify the output
    assert processed_image_obj is not None
    # Check that the result has an attribute 'image' which is a PIL Image
    assert hasattr(processed_image_obj, 'image')
    assert isinstance(processed_image_obj.image, Image.Image)
    # Verify the image has 3 channels (RGB)
    assert processed_image_obj.image.mode == 'RGB'
