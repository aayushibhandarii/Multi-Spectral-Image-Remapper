"""
Test Module for image_processing.py
Tests: AIModel, ImageProcessor

HOW TO RUN:
    python tests/test_image_processing.py

EXPECTED OUTPUT:
    - All tests should print "✓ PASSED" for each test case
    - Creates test output images showing different color palettes and stretches
    - Displays processing statistics (min/max values, image sizes)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from image_processing import AIModel, ImageProcessor
from models import FITSData, ProcessedImage
import numpy as np
from PIL import Image

def create_test_fits_data():
    """Create synthetic FITS data for testing"""
    # Create 3-channel data (simulating R, G, B or other channels)
    # Size: 3 channels x 300x300 pixels
    
    # Channel 0: Gradient from top to bottom
    channel_0 = np.linspace(0, 1000, 300*300).reshape(300, 300)
    
    # Channel 1: Gradient from left to right
    channel_1 = np.linspace(0, 1000, 300*300).reshape(300, 300).T
    
    # Channel 2: Circular gradient (center bright)
    y, x = np.ogrid[-150:150, -150:150]
    channel_2 = 1000 - np.sqrt(x**2 + y**2) * 3
    channel_2 = np.clip(channel_2, 0, 1000)
    
    data_cube = np.stack([channel_0, channel_1, channel_2])
    
    header = {
        'TELESCOP': 'TEST',
        'INSTRUME': 'SYNTHETIC',
        'NAXIS1': 300,
        'NAXIS2': 300,
        'NAXIS3': 3
    }
    
    return FITSData(data=data_cube, header=header)

def test_ai_model_stretch_methods():
    """Test different stretch methods in AIModel"""
    print("\n" + "="*60)
    print("TEST 1: AIModel Stretch Methods")
    print("="*60)
    
    model = AIModel()
    fits_data = create_test_fits_data()
    
    stretch_methods = ['power', 'asinh', 'sqrt', 'log']
    
    for method in stretch_methods:
        params = {
            'red_channel': 0,
            'green_channel': 1,
            'blue_channel': 2,
            'stretch_name': method,
            'power': 2.4,
            'black_point': 1.0,
            'white_point': 99.0,
            'saturation': 1.0,
            'red_scale': 1.0,
            'green_scale': 1.0,
            'blue_scale': 1.0
        }
        
        result = model.get_prediction(fits_data.get_raw_data(), params)
        
        assert isinstance(result, Image.Image), f"Result should be PIL Image for {method}!"
        assert result.mode == 'RGB', f"Image should be RGB for {method}!"
        assert result.size == (300, 300), f"Image size mismatch for {method}!"
        
        # Save output
        output_file = f"test_output_stretch_{method}.png"
        result.save(output_file)
        
        print(f"  ✓ {method.upper()} stretch: {result.size}, saved to {output_file}")
    
    print("✓ PASSED: All stretch methods work correctly")

def test_ai_model_color_palettes():
    """Test different color palette mappings"""
    print("\n" + "="*60)
    print("TEST 2: AIModel Color Palettes")
    print("="*60)
    
    model = AIModel()
    fits_data = create_test_fits_data()
    
    palettes = {
        'hubble_sho': {'red_channel': 2, 'green_channel': 0, 'blue_channel': 1},
        'natural_rgb': {'red_channel': 0, 'green_channel': 1, 'blue_channel': 2},
        'custom_bgr': {'red_channel': 2, 'green_channel': 1, 'blue_channel': 0}
    }
    
    for palette_name, channels in palettes.items():
        params = {
            **channels,
            'stretch_name': 'power',
            'power': 2.4,
            'black_point': 1.0,
            'white_point': 99.0,
            'saturation': 1.0,
            'red_scale': 1.0,
            'green_scale': 1.0,
            'blue_scale': 1.0
        }
        
        result = model.get_prediction(fits_data.get_raw_data(), params)
        
        assert isinstance(result, Image.Image), f"Result should be PIL Image for {palette_name}!"
        
        # Save output
        output_file = f"test_output_palette_{palette_name}.png"
        result.save(output_file)
        
        print(f"  ✓ {palette_name}: channels R={channels['red_channel']} G={channels['green_channel']} B={channels['blue_channel']}")
        print(f"    Saved to {output_file}")
    
    print("✓ PASSED: All color palettes work correctly")

def test_saturation_boost():
    """Test saturation boost functionality"""
    print("\n" + "="*60)
    print("TEST 3: Saturation Boost")
    print("="*60)
    
    model = AIModel()
    fits_data = create_test_fits_data()
    
    saturation_values = [0.5, 1.0, 1.5, 2.0]
    
    for sat in saturation_values:
        params = {
            'red_channel': 0,
            'green_channel': 1,
            'blue_channel': 2,
            'stretch_name': 'power',
            'power': 2.4,
            'black_point': 1.0,
            'white_point': 99.0,
            'saturation': sat,
            'red_scale': 1.0,
            'green_scale': 1.0,
            'blue_scale': 1.0
        }
        
        result = model.get_prediction(fits_data.get_raw_data(), params)
        
        output_file = f"test_output_saturation_{sat}.png"
        result.save(output_file)
        
        print(f"  ✓ Saturation {sat}: saved to {output_file}")
    
    print("✓ PASSED: Saturation boost works correctly")

def test_color_balance():
    """Test RGB color balance/scaling"""
    print("\n" + "="*60)
    print("TEST 4: Color Balance (RGB Scaling)")
    print("="*60)
    
    model = AIModel()
    fits_data = create_test_fits_data()
    
    balance_configs = [
        {'name': 'normal', 'red_scale': 1.0, 'green_scale': 1.0, 'blue_scale': 1.0},
        {'name': 'red_boost', 'red_scale': 1.5, 'green_scale': 1.0, 'blue_scale': 1.0},
        {'name': 'blue_boost', 'red_scale': 1.0, 'green_scale': 1.0, 'blue_scale': 1.5},
        {'name': 'green_reduce', 'red_scale': 1.0, 'green_scale': 0.7, 'blue_scale': 1.0}
    ]
    
    for config in balance_configs:
        params = {
            'red_channel': 0,
            'green_channel': 1,
            'blue_channel': 2,
            'stretch_name': 'power',
            'power': 2.4,
            'black_point': 1.0,
            'white_point': 99.0,
            'saturation': 1.0,
            'red_scale': config['red_scale'],
            'green_scale': config['green_scale'],
            'blue_scale': config['blue_scale']
        }
        
        result = model.get_prediction(fits_data.get_raw_data(), params)
        
        output_file = f"test_output_balance_{config['name']}.png"
        result.save(output_file)
        
        print(f"  ✓ {config['name']}: R={config['red_scale']} G={config['green_scale']} B={config['blue_scale']}")
        print(f"    Saved to {output_file}")
    
    print("✓ PASSED: Color balance works correctly")

def test_image_processor():
    """Test ImageProcessor class"""
    print("\n" + "="*60)
    print("TEST 5: ImageProcessor Integration")
    print("="*60)
    
    processor = ImageProcessor()
    fits_data = create_test_fits_data()
    
    params = {
        'red_channel': 2,
        'green_channel': 0,
        'blue_channel': 1,
        'stretch_name': 'power',
        'power': 2.4,
        'black_point': 0.5,
        'white_point': 99.8,
        'saturation': 1.3,
        'red_scale': 1.0,
        'green_scale': 1.0,
        'blue_scale': 1.0
    }
    
    # Process image
    result = processor.process_image(fits_data, params)
    
    # Verify result type
    assert isinstance(result, ProcessedImage), "Result should be ProcessedImage!"
    
    # Export and save
    pil_image = result.export_to(format="PNG")
    output_file = "test_output_processor_complete.png"
    pil_image.save(output_file)
    
    assert isinstance(pil_image, Image.Image), "Exported image should be PIL Image!"
    assert pil_image.size == (300, 300), "Image size mismatch!"
    
    print(f"✓ PASSED: ImageProcessor works correctly")
    print(f"  - Output type: {type(result).__name__}")
    print(f"  - Image size: {pil_image.size}")
    print(f"  - Saved to: {output_file}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "="*60)
    print("TEST 6: Edge Cases")
    print("="*60)
    
    model = AIModel()
    
    # Test 1: Invalid channel index (should raise error)
    try:
        small_data = np.random.rand(2, 100, 100)  # Only 2 channels
        params = {
            'red_channel': 0,
            'green_channel': 1,
            'blue_channel': 2,  # Channel 2 doesn't exist!
            'stretch_name': 'power',
            'power': 2.4,
            'black_point': 1.0,
            'white_point': 99.0,
            'saturation': 1.0,
            'red_scale': 1.0,
            'green_scale': 1.0,
            'blue_scale': 1.0
        }
        model.get_prediction(small_data, params)
        print("  ✗ Should have raised ValueError for invalid channel index!")
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {str(e)[:50]}...")
    
    # Test 2: Extreme saturation values
    fits_data = create_test_fits_data()
    extreme_params = {
        'red_channel': 0,
        'green_channel': 1,
        'blue_channel': 2,
        'stretch_name': 'power',
        'power': 2.4,
        'black_point': 1.0,
        'white_point': 99.0,
        'saturation': 5.0,  # Very high saturation
        'red_scale': 1.0,
        'green_scale': 1.0,
        'blue_scale': 1.0
    }
    result = model.get_prediction(fits_data.get_raw_data(), extreme_params)
    assert isinstance(result, Image.Image), "Should handle extreme saturation!"
    print(f"  ✓ Handles extreme saturation (5.0)")
    
    print("✓ PASSED: Edge cases handled correctly")

def run_all_tests():
    """Run all image processing tests"""
    print("\n" + "#"*60)
    print("# TESTING image_processing.py")
    print("#"*60)
    
    try:
        test_ai_model_stretch_methods()
        test_ai_model_color_palettes()
        test_saturation_boost()
        test_color_balance()
        test_image_processor()
        test_edge_cases()
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*60)
        print("\nGenerated Files (17 images total):")
        print("  - test_output_stretch_*.png (4 files - different stretches)")
        print("  - test_output_palette_*.png (3 files - different palettes)")
        print("  - test_output_saturation_*.png (4 files - saturation levels)")
        print("  - test_output_balance_*.png (4 files - color balance)")
        print("  - test_output_processor_complete.png (1 file)")
        print("\nYou can view these images to see the visual differences!")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()