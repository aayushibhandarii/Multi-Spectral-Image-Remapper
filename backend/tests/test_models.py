"""
Test Module for models.py
Tests: FITSData, ProcessedImage, HistoryItem

HOW TO RUN:
    python tests/test_models.py

EXPECTED OUTPUT:
    - All tests should print "✓ PASSED" for each test case
    - Creates a test image file: test_output_model.png
    - Prints HistoryItem data in JSON format
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import FITSData, ProcessedImage, HistoryItem
from PIL import Image
import numpy as np
from datetime import datetime

def test_fits_data():
    """Test FITSData class"""
    print("\n" + "="*60)
    print("TEST 1: FITSData Class")
    print("="*60)
    
    # Create sample data (3 channels, 100x100 pixels)
    sample_data = np.random.rand(3, 100, 100).astype(np.float32)
    sample_header = {'TELESCOP': 'Hubble', 'INSTRUME': 'WFC3', 'FILTER': 'F814W'}
    
    # Test instantiation
    fits_obj = FITSData(data=sample_data, header=sample_header)
    
    # Test get_raw_data
    retrieved_data = fits_obj.get_raw_data()
    
    # Assertions
    assert retrieved_data.shape == (3, 100, 100), "Data shape mismatch!"
    assert fits_obj.header['TELESCOP'] == 'Hubble', "Header data mismatch!"
    
    print(f"✓ PASSED: FITSData created successfully")
    print(f"  - Data shape: {retrieved_data.shape}")
    print(f"  - Header keys: {list(fits_obj.header.keys())}")
    print(f"  - Telescope: {fits_obj.header['TELESCOP']}")

def test_processed_image():
    """Test ProcessedImage class"""
    print("\n" + "="*60)
    print("TEST 2: ProcessedImage Class")
    print("="*60)
    
    # Create a sample PIL image (RGB, 200x200)
    sample_array = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    pil_img = Image.fromarray(sample_array, mode='RGB')
    
    # Test instantiation
    proc_img = ProcessedImage(pil_img)
    
    # Test export_to
    exported = proc_img.export_to(format="PNG")
    
    # Save to file for visual verification
    output_path = "test_output_model.png"
    exported.save(output_path)
    
    # Assertions
    assert exported.size == (200, 200), "Image size mismatch!"
    assert exported.mode == 'RGB', "Image mode mismatch!"
    assert os.path.exists(output_path), "Output file not created!"
    
    print(f"✓ PASSED: ProcessedImage created and exported")
    print(f"  - Image size: {exported.size}")
    print(f"  - Image mode: {exported.mode}")
    print(f"  - Saved to: {output_path}")

def test_history_item():
    """Test HistoryItem class"""
    print("\n" + "="*60)
    print("TEST 3: HistoryItem Class")
    print("="*60)
    
    # Test with auto timestamp
    settings = {
        'palette': 'hubble',
        'stretch': 'power',
        'saturation': 1.3
    }
    
    item1 = HistoryItem(
        input_filename="test_file.fits",
        settings_used=settings,
        status="Success"
    )
    
    # Test with manual timestamp
    custom_time = datetime(2025, 1, 15, 14, 30, 0)
    item2 = HistoryItem(
        input_filename="another_file.fits",
        settings_used={'palette': 'natural'},
        status="Failed",
        timestamp=custom_time
    )
    
    # Test to_dict method
    dict1 = item1.to_dict()
    dict2 = item2.to_dict()
    
    # Assertions
    assert 'timestamp' in dict1, "Missing timestamp in dict!"
    assert dict1['filename'] == "test_file.fits", "Filename mismatch!"
    assert dict1['settings']['palette'] == 'hubble', "Settings mismatch!"
    assert dict1['status'] == "Success", "Status mismatch!"
    assert dict2['timestamp'] == custom_time.isoformat(), "Custom timestamp mismatch!"
    
    print(f"✓ PASSED: HistoryItem created and serialized")
    print(f"  - Item 1 (auto timestamp):")
    print(f"    Filename: {dict1['filename']}")
    print(f"    Status: {dict1['status']}")
    print(f"    Settings: {dict1['settings']}")
    print(f"  - Item 2 (custom timestamp):")
    print(f"    Timestamp: {dict2['timestamp']}")
    print(f"    Status: {dict2['status']}")

def run_all_tests():
    """Run all model tests"""
    print("\n" + "#"*60)
    print("# TESTING models.py")
    print("#"*60)
    
    try:
        test_fits_data()
        test_processed_image()
        test_history_item()
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*60)
        print("\nGenerated Files:")
        print("  - test_output_model.png (sample processed image)")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()