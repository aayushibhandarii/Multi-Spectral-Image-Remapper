"""
Test Module for controller.py
Tests: AppController with REAL FITS files

HOW TO RUN:
    python tests/test_controller.py

REQUIREMENTS:
    - FITS test files must exist in test_data/ folder:
        * test_data/h_m51_b_s05_drz_sci.fits
        * test_data/h_m51_i_s05_drz_sci.fits
        * test_data/h_m51_v_s05_drz_sci.fits

EXPECTED OUTPUT:
    - All tests should print "✓ PASSED"
    - Creates colorized images from real FITS data
    - Generates Base64 encoded images
    - Updates history.json
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from controller import AppController
import base64
import json
from io import BytesIO
from PIL import Image

# Mock file storage object for testing
class MockFileStorage:
    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename
    
    def save(self, destination):
        """Copy file to destination"""
        import shutil
        shutil.copy(self.filepath, destination)

def test_controller_initialization():
    """Test AppController initialization"""
    print("\n" + "="*60)
    print("TEST 1: AppController Initialization")
    print("="*60)
    
    controller = AppController()
    
    assert controller.image_processor is not None, "ImageProcessor not initialized!"
    assert controller.history_manager is not None, "HistoryManager not initialized!"
    assert os.path.exists('uploads'), "Upload folder not created!"
    assert os.path.exists('static'), "Static folder not created!"
    
    print("✓ PASSED: AppController initialized successfully")
    print(f"  - ImageProcessor: {type(controller.image_processor).__name__}")
    print(f"  - HistoryManager: {type(controller.history_manager).__name__}")
    print(f"  - Upload folder exists: {os.path.exists('uploads')}")
    print(f"  - Static folder exists: {os.path.exists('static')}")

def test_colorize_with_real_fits():
    """Test colorization with real FITS files"""
    print("\n" + "="*60)
    print("TEST 2: Colorize Real FITS Files")
    print("="*60)
    
    # Check if test files exist
    test_files = [
        'test_data/h_m51_b_s05_drz_sci.fits',
        'test_data/h_m51_i_s05_drz_sci.fits',
        'test_data/h_m51_v_s05_drz_sci.fits'
    ]
    
    for filepath in test_files:
        if not os.path.exists(filepath):
            print(f"✗ SKIPPED: Test file not found: {filepath}")
            print("  Please ensure FITS files are in test_data/ folder")
            return
    
    print("✓ All test FITS files found")
    
    # Create mock file storage objects
    files = {
        'red': MockFileStorage(test_files[0], 'h_m51_b_s05_drz_sci.fits'),
        'green': MockFileStorage(test_files[1], 'h_m51_i_s05_drz_sci.fits'),
        'blue': MockFileStorage(test_files[2], 'h_m51_v_s05_drz_sci.fits')
    }
    
    # Test with 'natural' palette
    model_params = {'palette': 'natural'}
    
    controller = AppController()
    result, error = controller.colorize_layers(files, model_params)
    
    assert error is None, f"Colorization failed: {error}"
    assert result is not None, "Result should not be None!"
    assert 'imageData' in result, "Result should contain imageData!"
    assert 'metadata' in result, "Result should contain metadata!"
    
    # Verify imageData is valid base64
    assert result['imageData'].startswith('data:image/png;base64,'), "Invalid base64 prefix!"
    
    # Decode and verify it's a valid image
    base64_str = result['imageData'].split(',')[1]
    image_bytes = base64.b64decode(base64_str)
    img = Image.open(BytesIO(image_bytes))
    
    assert img.mode == 'RGB', "Image should be RGB!"
    assert img.size[0] > 0 and img.size[1] > 0, "Image should have valid dimensions!"
    
    # Save the output
    output_file = "test_output_controller_natural.png"
    img.save(output_file)
    
    print("✓ PASSED: Real FITS files colorized successfully")
    print(f"  - Image size: {img.size}")
    print(f"  - Image mode: {img.mode}")
    print(f"  - Metadata keys: {len(result['metadata'])}")
    print(f"  - Saved to: {output_file}")

def test_different_palettes():
    """Test all available color palettes"""
    print("\n" + "="*60)
    print("TEST 3: Different Color Palettes")
    print("="*60)
    
    test_files = [
        'test_data/h_m51_b_s05_drz_sci.fits',
        'test_data/h_m51_i_s05_drz_sci.fits',
        'test_data/h_m51_v_s05_drz_sci.fits'
    ]
    
    # Check if files exist
    if not all(os.path.exists(f) for f in test_files):
        print("✗ SKIPPED: FITS test files not found")
        return
    
    palettes = ['hubble', 'natural', 'custom']
    controller = AppController()
    
    for palette in palettes:
        files = {
            'red': MockFileStorage(test_files[0], 'h_m51_b_s05_drz_sci.fits'),
            'green': MockFileStorage(test_files[1], 'h_m51_i_s05_drz_sci.fits'),
            'blue': MockFileStorage(test_files[2], 'h_m51_v_s05_drz_sci.fits')
        }
        
        model_params = {'palette': palette}
        result, error = controller.colorize_layers(files, model_params)
        
        assert error is None, f"Failed for palette {palette}: {error}"
        
        # Save output
        base64_str = result['imageData'].split(',')[1]
        image_bytes = base64.b64decode(base64_str)
        img = Image.open(BytesIO(image_bytes))
        
        output_file = f"test_output_controller_{palette}.png"
        img.save(output_file)
        
        print(f"  ✓ {palette.upper()} palette: {img.size}, saved to {output_file}")
    
    print("✓ PASSED: All palettes work correctly")

def test_custom_parameters():
    """Test with custom processing parameters"""
    print("\n" + "="*60)
    print("TEST 4: Custom Processing Parameters")
    print("="*60)
    
    test_files = [
        'test_data/h_m51_b_s05_drz_sci.fits',
        'test_data/h_m51_i_s05_drz_sci.fits',
        'test_data/h_m51_v_s05_drz_sci.fits'
    ]
    
    if not all(os.path.exists(f) for f in test_files):
        print("✗ SKIPPED: FITS test files not found")
        return
    
    files = {
        'red': MockFileStorage(test_files[0], 'h_m51_b_s05_drz_sci.fits'),
        'green': MockFileStorage(test_files[1], 'h_m51_i_s05_drz_sci.fits'),
        'blue': MockFileStorage(test_files[2], 'h_m51_v_s05_drz_sci.fits')
    }
    
    # Test with custom parameters
    custom_params = {
        'palette': 'natural',
        'stretch_name': 'asinh',
        'power': 3.0,
        'black_point': 1.0,
        'white_point': 99.5,
        'saturation': 1.5,
        'red_scale': 1.2,
        'green_scale': 1.0,
        'blue_scale': 0.9
    }
    
    controller = AppController()
    result, error = controller.colorize_layers(files, custom_params)
    
    assert error is None, f"Custom params failed: {error}"
    
    # Save output
    base64_str = result['imageData'].split(',')[1]
    image_bytes = base64.b64decode(base64_str)
    img = Image.open(BytesIO(image_bytes))
    
    output_file = "test_output_controller_custom_params.png"
    img.save(output_file)
    
    print("✓ PASSED: Custom parameters work correctly")
    print(f"  - Stretch: {custom_params['stretch_name']}")
    print(f"  - Saturation: {custom_params['saturation']}")
    print(f"  - Color scales: R={custom_params['red_scale']} G={custom_params['green_scale']} B={custom_params['blue_scale']}")
    print(f"  - Saved to: {output_file}")

def test_history_logging():
    """Test that history is logged correctly"""
    print("\n" + "="*60)
    print("TEST 5: History Logging")
    print("="*60)
    
    test_files = [
        'test_data/h_m51_b_s05_drz_sci.fits',
        'test_data/h_m51_i_s05_drz_sci.fits',
        'test_data/h_m51_v_s05_drz_sci.fits'
    ]
    
    if not all(os.path.exists(f) for f in test_files):
        print("✗ SKIPPED: FITS test files not found")
        return
    
    controller = AppController()
    
    # Get initial history count
    initial_history = controller.get_history()
    initial_count = len(initial_history)
    
    # Perform colorization
    files = {
        'red': MockFileStorage(test_files[0], 'h_m51_b_s05_drz_sci.fits'),
        'green': MockFileStorage(test_files[1], 'h_m51_i_s05_drz_sci.fits'),
        'blue': MockFileStorage(test_files[2], 'h_m51_v_s05_drz_sci.fits')
    }
    
    model_params = {'palette': 'hubble'}
    result, error = controller.colorize_layers(files, model_params)
    
    # Get updated history
    updated_history = controller.get_history()
    
    assert len(updated_history) == initial_count + 1, "History count should increase by 1!"
    assert updated_history[0]['status'] == 'Success', "Status should be Success!"
    assert 'h_m51_b_s05_drz_sci.fits' in updated_history[0]['filename'], "Filename should be in history!"
    
    print("✓ PASSED: History logged correctly")
    print(f"  - Initial count: {initial_count}")
    print(f"  - Updated count: {len(updated_history)}")
    print(f"  - Latest entry: {updated_history[0]['filename']}")
    print(f"  - Status: {updated_history[0]['status']}")

def test_metadata_extraction():
    """Test that FITS metadata is extracted correctly"""
    print("\n" + "="*60)
    print("TEST 6: FITS Metadata Extraction")
    print("="*60)
    
    test_files = [
        'test_data/h_m51_b_s05_drz_sci.fits',
        'test_data/h_m51_i_s05_drz_sci.fits',
        'test_data/h_m51_v_s05_drz_sci.fits'
    ]
    
    if not all(os.path.exists(f) for f in test_files):
        print("✗ SKIPPED: FITS test files not found")
        return
    
    files = {
        'red': MockFileStorage(test_files[0], 'h_m51_b_s05_drz_sci.fits'),
        'green': MockFileStorage(test_files[1], 'h_m51_i_s05_drz_sci.fits'),
        'blue': MockFileStorage(test_files[2], 'h_m51_v_s05_drz_sci.fits')
    }
    
    controller = AppController()
    result, error = controller.colorize_layers(files, {'palette': 'natural'})
    
    assert 'metadata' in result, "Result should contain metadata!"
    metadata = result['metadata']
    
    assert isinstance(metadata, dict), "Metadata should be a dictionary!"
    assert len(metadata) > 0, "Metadata should not be empty!"
    
    print("✓ PASSED: Metadata extracted successfully")
    print(f"  - Number of metadata keys: {len(metadata)}")
    print(f"  - Sample metadata keys: {list(metadata.keys())[:10]}")

def run_all_tests():
    """Run all controller tests"""
    print("\n" + "#"*60)
    print("# TESTING controller.py")
    print("#"*60)
    
    try:
        test_controller_initialization()
        test_colorize_with_real_fits()
        test_different_palettes()
        test_custom_parameters()
        test_history_logging()
        test_metadata_extraction()
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*60)
        print("\nGenerated Files:")
        print("  - test_output_controller_natural.png")
        print("  - test_output_controller_hubble.png")
        print("  - test_output_controller_custom.png")
        print("  - test_output_controller_custom_params.png")
        print("  - history.json (updated)")
        print("\nThese are real colorized astronomical images from M51!")
        
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