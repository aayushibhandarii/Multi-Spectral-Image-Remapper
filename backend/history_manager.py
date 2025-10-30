
import json
import os
from models import HistoryItem

HISTORY_FILE = 'history.json'

class HistoryManager:
    """Manages the user's processing history."""
    def __init__(self):
        self.history_log = self._load_history()

    def _load_history(self):
        if not os.path.exists(HISTORY_FILE):
            return []
        with open(HISTORY_FILE, 'r') as f:
            try:
                return [HistoryItem(**item) for item in json.load(f)]
            except (json.JSONDecodeError, TypeError):
                return [] # Return empty list if file is corrupt or not in the expected format

    def _save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([item.to_dict() for item in self.history_log], f, indent=2)

    def add_entry(self, item):
        self.history_log.insert(0, item)
        self._save_history()

    def get_history(self):
        return [item.to_dict() for item in self.history_log]

    def clear_history(self):
        self.history_log = []
        self._save_history()
