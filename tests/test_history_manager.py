
import os
import json
from datetime import datetime
import pytest
from backend.history_manager import HistoryManager, HistoryItem

@pytest.fixture
def history_file(tmp_path):
    """Provides a temporary file path for isolated test runs."""
    return tmp_path / "test_history.json"

def test_add_and_get_entry(history_file):
    """
    Tests if a new entry is correctly added and retrieved.
    Input: A HistoryItem object.
    Output: The history log (list of dicts) should contain the added item.
    """
    manager = HistoryManager(history_file)
    assert manager.get_history() == [] # Starts empty

    item = HistoryItem(
        timestamp=datetime.now().isoformat(),
        input_file_name="test_image.fits",
        settings_used={"contrast": 1.5},
        output_thumbnail_path="thumb.jpg"
    )
    manager.add_entry(item)

    history = manager.get_history()
    assert len(history) == 1
    assert history[0]["input_file_name"] == "test_image.fits"
    assert history[0]["settings_used"]["contrast"] == 1.5

def test_clear_history(history_file):
    """
    Tests if the history is correctly cleared.
    Input: A history log with one item.
    Output: An empty history log.
    """
    manager = HistoryManager(history_file)
    item = HistoryItem(
        timestamp=datetime.now().isoformat(),
        input_file_name="test_image.fits",
        settings_used={},
        output_thumbnail_path="thumb.jpg"
    )
    manager.add_entry(item)
    assert len(manager.get_history()) == 1 # Verify it's not empty

    manager.clear_history()
    assert len(manager.get_history()) == 0 # Verify it's empty
