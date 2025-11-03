
import pytest
import numpy as np
from PIL import Image
from astropy.visualization import AsinhStretch, SqrtStretch, LinearStretch

from backend.colorizer import colorize_fits, get_stretch_function

@pytest.fixture
def mock_fits_cube():
    """
    Provides a simple, predictable 3D NumPy array to simulate FITS data.
    Shape: (3, 10, 10) -> 3 channels, 10x10 pixels each.
    """
    # Create a gradient image in each channel
    channel1 = np.ones((10, 10)) * 0.25
    channel2 = np.ones((10, 10)) * 0.50
    channel3 = np.ones((10, 10)) * 0.75
    return np.stack([channel1, channel2, channel3], axis=0)

def test_colorize_fits(mock_fits_cube):
    """
    Tests the main colorization function.
    Input: A 3D NumPy array (a mock FITS data cube).
    Output: A PIL Image object in RGB mode.
    """
    red_channel = 0
    green_channel = 1
    blue_channel = 2

    # Run the colorization
    result_image = colorize_fits(
        mock_fits_cube, 
        red_channel, 
        green_channel, 
        blue_channel
    )

    # Verify the output type and properties
    assert isinstance(result_image, Image.Image)
    assert result_image.mode == 'RGB'
    assert result_image.size == (10, 10) # Width, Height

def test_colorize_fits_invalid_channels(mock_fits_cube):
    """
    Tests that the function raises an error for invalid channel indices.
    Input: A mock FITS data cube and channel indices that are out of bounds.
    Output: A ValueError.
    """
    with pytest.raises(ValueError):
        # Channel 3 does not exist in the mock_fits_cube
        colorize_fits(mock_fits_cube, red_channel=0, green_channel=1, blue_channel=3)

@pytest.mark.parametrize("stretch_name, expected_type", [
    ("asinh", AsinhStretch),
    ("sqrt", SqrtStretch),
    ("linear", LinearStretch),
    ("invalid_name", AsinhStretch), # Test default case
])
def test_get_stretch_function(stretch_name, expected_type):
    """
    Tests the stretch function selector.
    Input: The name of a stretch function.
    Output: The corresponding stretch object from astropy.
    """
    stretch_func = get_stretch_function(stretch_name)
    assert isinstance(stretch_func, expected_type)
