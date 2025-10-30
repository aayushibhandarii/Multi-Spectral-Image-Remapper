
from datetime import datetime
from PIL import Image

class FITSData:
    """Holds the raw FITS data from an uploaded file."""
    def __init__(self, data, header):
        self.data = data
        self.header = header

    def get_raw_data(self):
        return self.data

class ProcessedImage:
    """Holds the final, colorized RGB image and handles adjustments."""
    def __init__(self, pil_image):
        self.pil_image = pil_image

    def export_to(self, format="PNG"):
        """Exports the image to a specified format."""
        # In a real scenario, this would handle different formats.
        # For now, it just returns the PIL image.
        return self.pil_image

class HistoryItem:
    """A simple data object representing one entry in the history log."""
    def __init__(self, input_filename, settings_used, status, timestamp=None):
        self.timestamp = timestamp or datetime.now()
        self.input_filename = input_filename
        self.settings_used = settings_used
        self.status = status

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "filename": self.input_filename,
            "settings": self.settings_used,
            "status": self.status,
        }
