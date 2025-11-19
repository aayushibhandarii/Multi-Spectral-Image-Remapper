# ML Denoising Setup Instructions

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

If you have a CUDA-capable GPU (recommended for faster processing):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Step 2: Create Models Directory
```bash
mkdir models
```

## Step 3: Download Pre-trained DnCNN Weights (Optional but Recommended)

### Option A: Use Pre-trained Weights (Best Results)

Download pre-trained DnCNN model:

1. Visit: https://github.com/cszn/DnCNN
2. Download `dncnn_50.pth` or `dncnn_25.pth`
3. Save as `models/dncnn_astro.pth`

OR use this direct link:
```bash
wget https://github.com/cszn/DnCNN/raw/master/TrainingCodes/dncnn_pytorch/logs/DnCNN-S-50/model_best.pth -O models/dncnn_astro.pth
```

### Option B: Train Your Own (Advanced)

If you want to train on astronomical data specifically:
- Collect noisy/clean FITS image pairs
- Use the training script in the DnCNN repository
- This requires significant computational resources

### Option C: Use Random Initialization (Works but Less Effective)

The code will work without pre-trained weights, but denoising quality will be lower. The model will still provide some noise reduction through its architecture.

## Step 4: Project Structure

Your project should look like this:
```
your_project/
├── models/
│   └── dncnn_astro.pth          # ML model weights (optional)
├── uploads/                      # FITS uploads folder
├── static/                       # Static files
├── controller.py                 # Updated with denoising
├── image_processing.py           # Updated with denoising
├── denoiser.py                   # NEW: ML denoising module
├── models.py                     # Data models (unchanged)
├── history_manager.py            # History tracking (unchanged)
└── requirements.txt              # Updated dependencies
```

## Step 5: Test the Denoising

Run your Flask app and upload FITS files. You should see console output like:
```
🤖 Applying ML-based noise reduction...
  Denoising channel 1/3...
  Denoising channel 2/3...
  Denoising channel 3/3...
✓ Denoising complete!
```

## Step 6: Disable Denoising (Optional)

If you want to compare results or disable denoising:

Add `"use_denoising": false` to your request parameters from the frontend.

## GPU Acceleration Notes

- **CPU-only**: Works fine but slower (~2-5 seconds per channel)
- **GPU (CUDA)**: Much faster (~0.5-1 second per channel)
- The code automatically detects and uses GPU if available

## Troubleshooting

### "Model file not found"
- This is fine! The code will work with random initialization
- For better results, download pre-trained weights (see Step 3)

### "CUDA out of memory"
- Reduce image size before processing
- Process channels one at a time (already implemented)
- Use CPU instead: set `CUDA_VISIBLE_DEVICES=""` environment variable

### "Import error: No module named torch"
- Run: `pip install torch torchvision`

## What Changed?

1. **denoiser.py**: New module with DnCNN neural network for noise reduction
2. **image_processing.py**: Added denoising step before colorization
3. **controller.py**: Added `use_denoising` parameter
4. **requirements.txt**: Added PyTorch dependencies

All other files remain unchanged!