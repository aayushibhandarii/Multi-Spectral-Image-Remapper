import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import os

class DnCNN(nn.Module):
    """DnCNN denoising network for astronomical images."""
    def __init__(self, channels=1, num_of_layers=17):
        super(DnCNN, self).__init__()
        kernel_size = 3
        padding = 1
        features = 64
        layers = []
        layers.append(nn.Conv2d(in_channels=channels, out_channels=features, 
                                kernel_size=kernel_size, padding=padding, bias=False))
        layers.append(nn.ReLU(inplace=True))
        for _ in range(num_of_layers-2):
            layers.append(nn.Conv2d(in_channels=features, out_channels=features, 
                                    kernel_size=kernel_size, padding=padding, bias=False))
            layers.append(nn.BatchNorm2d(features))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Conv2d(in_channels=features, out_channels=channels, 
                                kernel_size=kernel_size, padding=padding, bias=False))
        self.dncnn = nn.Sequential(*layers)
    
    def forward(self, x):
        out = self.dncnn(x)
        return x - out  # Residual learning


class AstronomicalDenoiser:
    """Handles ML-based denoising of FITS data."""
    
    def __init__(self, model_path='models/dncnn_astro.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = DnCNN(channels=1, num_of_layers=17)
        
        # Load pre-trained weights if available
        if os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"✓ Loaded pre-trained denoising model from {model_path}")
            except Exception as e:
                print(f"⚠ Could not load model weights: {e}")
                print("  Using randomly initialized model (will still reduce some noise)")
        else:
            print(f"⚠ Model file not found at {model_path}")
            print("  Using randomly initialized model")
            print("  Download pre-trained weights from: https://github.com/cszn/DnCNN")
        
        self.model.to(self.device)
        self.model.eval()
    
    def denoise_channel(self, data):
        """Denoise a single 2D channel."""
        # Handle NaN and inf
        data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Normalize to [0, 1] range for the model
        data_min = data.min()
        data_max = data.max()
        data_range = data_max - data_min
        
        if data_range == 0:
            return data  # Avoid division by zero
        
        normalized = (data - data_min) / data_range
        
        # Convert to tensor
        tensor_data = torch.from_numpy(normalized).float().unsqueeze(0).unsqueeze(0)
        tensor_data = tensor_data.to(self.device)
        
        # Denoise
        with torch.no_grad():
            denoised = self.model(tensor_data)
        
        # Convert back to numpy
        denoised = denoised.cpu().squeeze().numpy()
        
        # Denormalize
        denoised = denoised * data_range + data_min
        
        return denoised.astype(np.float32)
    
    def denoise_fits_cube(self, fits_data):
        """
        Denoise a 3D FITS data cube (multiple channels).
        
        Args:
            fits_data: numpy array of shape (channels, height, width)
        
        Returns:
            Denoised numpy array of same shape
        """
        if fits_data.ndim != 3:
            raise ValueError("Expected 3D data cube (channels, height, width)")
        
        denoised_cube = np.zeros_like(fits_data)
        
        # Denoise each channel separately
        for i in range(fits_data.shape[0]):
            print(f"  Denoising channel {i+1}/{fits_data.shape[0]}...")
            denoised_cube[i] = self.denoise_channel(fits_data[i])
        
        return denoised_cube