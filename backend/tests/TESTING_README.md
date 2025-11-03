# Astro Image Colorizer - Module Testing Guide

## 📁 Directory Structure

```
backend/
├── tests/                          # Create this folder
│   ├── test_models.py
│   ├── test_history_manager.py
│   ├── test_image_processing.py
│   ├── test_controller.py
│   └── run_all_tests.py
├── test_data/                      # Your existing FITS files
│   ├── h_m51_b_s05_drz_sci.fits
│   ├── h_m51_i_s05_drz_sci.fits
│   └── h_m51_v_s05_drz_sci.fits
├── models.py
├── history_manager.py
├── image_processing.py
├── controller.py
└── app.py
```

## 🚀 Setup Instructions

### 1. Create the tests folder
```bash
cd backend
mkdir tests
```

### 2. Place all test files in the tests/ folder
- test_models.py
- test_history_manager.py
- test_image_processing.py
- test_controller.py
- run_all_tests.py

### 3. Install required dependencies (if not already installed)
```bash
pip install numpy pillow astropy flask flask-cors
```

## 🧪 Running Tests

### Option 1: Run Individual Tests

**Test models.py:**
```bash
python tests/test_models.py
```
- **Expected Output**: Creates `test_output_model.png`
- **Tests**: FITSData, ProcessedImage, HistoryItem classes

**Test history_manager.py:**
```bash
python tests/test_history_manager.py
```
- **Expected Output**: Creates/modifies `history.json`
- **Tests**: Adding, retrieving, clearing history

**Test image_processing.py:**
```bash
python tests/test_image_processing.py
```
- **Expected Output**: Creates 17 PNG images with different processing settings
- **Tests**: AIModel stretch methods, color palettes, saturation, color balance

**Test controller.py:**
```bash
python tests/test_controller.py
```
- **Expected Output**: Creates 4 colorized M51 galaxy images
- **Tests**: Full integration with real FITS files
- **⚠️ Requires**: FITS files in `test_data/` folder

### Option 2: Run All Tests at Once

```bash
python tests/run_all_tests.py
```

This runs all tests sequentially and provides a summary report.

## 📊 Expected Test Outputs

### test_models.py
| File | Description |
|------|-------------|
| `test_output_model.png` | Sample processed image (200x200) |

### test_history_manager.py
| File | Description |
|------|-------------|
| `history.json` | History log with test entries |

### test_image_processing.py
| Files | Description |
|-------|-------------|
| `test_output_stretch_power.png` | Power stretch method |
| `test_output_stretch_asinh.png` | Asinh stretch method |
| `test_output_stretch_sqrt.png` | Square root stretch |
| `test_output_stretch_log.png` | Logarithmic stretch |
| `test_output_palette_hubble_sho.png` | Hubble palette (SHO) |
| `test_output_palette_natural_rgb.png` | Natural RGB palette |
| `test_output_palette_custom_bgr.png` | Custom BGR palette |
| `test_output_saturation_0.5.png` | Low saturation |
| `test_output_saturation_1.0.png` | Normal saturation |
| `test_output_saturation_1.5.png` | High saturation |
| `test_output_saturation_2.0.png` | Very high saturation |
| `test_output_balance_normal.png` | Normal color balance |
| `test_output_balance_red_boost.png` | Red channel boosted |
| `test_output_balance_blue_boost.png` | Blue channel boosted |
| `test_output_balance_green_reduce.png` | Green channel reduced |
| `test_output_processor_complete.png` | Complete processor test |

### test_controller.py
| Files | Description |
|-------|-------------|
| `test_output_controller_natural.png` | M51 with natural palette |
| `test_output_controller_hubble.png` | M51 with Hubble palette |
| `test_output_controller_custom.png` | M51 with custom palette |
| `test_output_controller_custom_params.png` | M51 with custom parameters |

## 📸 Taking Screenshots

### For Each Module Test:

1. **Run the test**:
   ```bash
   python tests/test_[module_name].py
   ```

2. **Capture the terminal output** showing:
   - All test names
   - ✓ PASSED messages
   - File creation confirmations

3. **View the generated images**:
   - Open the PNG files in an image viewer
   - Take screenshots of interesting outputs

### Screenshot Checklist:

- [ ] Terminal output showing all tests passed
- [ ] Sample of generated images (especially from controller tests)
- [ ] `history.json` file contents
- [ ] File listing showing all generated outputs

## 🔧 Adding More Test Data

### To add more FITS test files:

1. **Place new FITS files in `test_data/` folder**:
   ```
   test_data/
   ├── my_new_file_red.fits
   ├── my_new_file_green.fits
   └── my_new_file_blue.fits
   ```

2. **Modify `test_controller.py`**:
   ```python
   test_files = [
       'test_data/my_new_file_red.fits',
       'test_data/my_new_file_green.fits',
       'test_data/my_new_file_blue.fits'
   ]
   ```

3. **Run the controller test**:
   ```bash
   python tests/test_controller.py
   ```

### To test different palettes or settings:

Edit the `custom_params` dictionary in `test_controller.py`:

```python
custom_params = {
    'palette': 'hubble',           # or 'natural', 'custom'
    'stretch_name': 'power',       # or 'asinh', 'sqrt', 'log'
    'power': 2.4,                  # 1.0 to 5.0
    'black_point': 0.5,            # 0.0 to 5.0
    'white_point': 99.8,           # 95.0 to 100.0
    'saturation': 1.3,             # 0.0 to 3.0
    'red_scale': 1.0,              # 0.5 to 2.0
    'green_scale': 1.0,            # 0.5 to 2.0
    'blue_scale': 1.0              # 0.5 to 2.0
}
```

## ✅ Test Verification

Each test file includes assertions that verify:
- Correct data types
- Expected output formats
- Valid image dimensions
- Proper error handling
- File creation

### How to verify tests passed:

1. **Check terminal output** for:
   ```
   ✓✓✓ ALL TESTS PASSED ✓✓✓
   ```

2. **Verify generated files exist**:
   ```bash
   ls test_output_*.png
   ls history.json
   ```

3. **Open and inspect images** to ensure they look correct

## 🐛 Troubleshooting

### "Test file not found" error:
- Make sure you're in the `backend` directory when running tests
- Check that test files are in `backend/tests/` folder

### "FITS test files not found" error:
- Ensure FITS files are in `backend/test_data/` folder
- Check file names match exactly

### "ModuleNotFoundError" error:
- Install missing dependencies: `pip install numpy pillow astropy`
- Make sure you're using the correct Python environment

### Tests pass but no images generated:
- Check current directory for output files
- Look for error messages in terminal output

## 📝 Notes

- All tests create output files in the **current directory** where you run them
- Run tests from the `backend` directory for consistency
- Generated images are **NOT** deleted automatically - you may want to clean them up periodically
- `history.json` accumulates entries - use the clear_history test to reset if needed

## 🎯 Success Criteria

A successful test run should show:
- ✓ All assertions passed
- ✓ All expected files generated
- ✓ Images are valid and viewable
- ✓ No error messages or exceptions
- ✓ Terminal output matches expected format

Happy Testing! 🚀
