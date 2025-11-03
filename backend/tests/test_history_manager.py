"""
Test Module for history_manager.py
Tests: HistoryManager class

HOW TO RUN:
    python tests/test_history_manager.py

EXPECTED OUTPUT:
    - All tests should print "✓ PASSED" for each test case
    - Creates/modifies history.json file
    - Prints history entries in readable format
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from history_manager import HistoryManager
from models import HistoryItem
from datetime import datetime
import json

def cleanup_history_file():
    """Remove history.json if it exists"""
    if os.path.exists('history.json'):
        os.remove('history.json')

def test_initialization():
    """Test HistoryManager initialization"""
    print("\n" + "="*60)
    print("TEST 1: HistoryManager Initialization")
    print("="*60)
    
    cleanup_history_file()
    
    # Test initialization with no existing file
    manager = HistoryManager()
    
    assert manager.history_log == [], "History should be empty on first init!"
    assert not os.path.exists('history.json'), "History file shouldn't exist yet!"
    
    print("✓ PASSED: HistoryManager initialized with empty history")

def test_add_entry():
    """Test adding entries to history"""
    print("\n" + "="*60)
    print("TEST 2: Adding History Entries")
    print("="*60)
    
    cleanup_history_file()
    manager = HistoryManager()
    
    # Add first entry
    item1 = HistoryItem(
        input_filename="file1.fits, file2.fits, file3.fits",
        settings_used={'palette': 'hubble', 'power': 2.4},
        status="Success"
    )
    manager.add_entry(item1)
    
    # Add second entry
    item2 = HistoryItem(
        input_filename="fileA.fits, fileB.fits, fileC.fits",
        settings_used={'palette': 'natural', 'saturation': 1.5},
        status="Success"
    )
    manager.add_entry(item2)
    
    # Verify
    assert len(manager.history_log) == 2, "Should have 2 entries!"
    assert os.path.exists('history.json'), "History file should be created!"
    assert manager.history_log[0].input_filename == "fileA.fits, fileB.fits, fileC.fits", "Latest entry should be first!"
    
    print("✓ PASSED: Entries added successfully")
    print(f"  - Total entries: {len(manager.history_log)}")
    print(f"  - Latest entry: {manager.history_log[0].input_filename}")
    print(f"  - History file exists: {os.path.exists('history.json')}")

def test_get_history():
    """Test retrieving history"""
    print("\n" + "="*60)
    print("TEST 3: Retrieving History")
    print("="*60)
    
    manager = HistoryManager()
    history = manager.get_history()
    
    assert isinstance(history, list), "History should be a list!"
    assert len(history) > 0, "History should have entries!"
    assert 'timestamp' in history[0], "Entry should have timestamp!"
    assert 'filename' in history[0], "Entry should have filename!"
    assert 'settings' in history[0], "Entry should have settings!"
    assert 'status' in history[0], "Entry should have status!"
    
    print("✓ PASSED: History retrieved successfully")
    print(f"  - Number of entries: {len(history)}")
    print(f"  - First entry:")
    for key, value in history[0].items():
        print(f"    {key}: {value}")

def test_persistence():
    """Test history persistence across instances"""
    print("\n" + "="*60)
    print("TEST 4: History Persistence")
    print("="*60)
    
    # Create first manager and add entry
    manager1 = HistoryManager()
    initial_count = len(manager1.history_log)
    
    item = HistoryItem(
        input_filename="persistence_test.fits",
        settings_used={'test': 'persistence'},
        status="Success"
    )
    manager1.add_entry(item)
    
    # Create second manager (should load from file)
    manager2 = HistoryManager()
    
    assert len(manager2.history_log) == initial_count + 1, "New manager should load saved history!"
    assert manager2.history_log[0].input_filename == "persistence_test.fits", "Latest entry should persist!"
    
    print("✓ PASSED: History persists across instances")
    print(f"  - Entries in first manager: {initial_count + 1}")
    print(f"  - Entries in second manager: {len(manager2.history_log)}")

def test_clear_history():
    """Test clearing history"""
    print("\n" + "="*60)
    print("TEST 5: Clearing History")
    print("="*60)
    
    manager = HistoryManager()
    
    # Add some entries first
    for i in range(3):
        item = HistoryItem(
            input_filename=f"file{i}.fits",
            settings_used={'index': i},
            status="Success"
        )
        manager.add_entry(item)
    
    assert len(manager.history_log) > 0, "Should have entries before clearing!"
    
    # Clear history
    manager.clear_history()
    
    assert len(manager.history_log) == 0, "History should be empty after clearing!"
    
    # Verify persistence
    manager2 = HistoryManager()
    assert len(manager2.history_log) == 0, "Cleared history should persist!"
    
    print("✓ PASSED: History cleared successfully")
    print(f"  - Entries after clearing: {len(manager.history_log)}")

def test_corrupt_file_handling():
    """Test handling of corrupt history file"""
    print("\n" + "="*60)
    print("TEST 6: Corrupt File Handling")
    print("="*60)
    
    # Create corrupt history file
    with open('history.json', 'w') as f:
        f.write("This is not valid JSON {{{")
    
    # Should handle gracefully
    manager = HistoryManager()
    
    assert manager.history_log == [], "Should return empty list for corrupt file!"
    
    print("✓ PASSED: Corrupt file handled gracefully")
    print(f"  - Loaded history: {len(manager.history_log)} entries")

def display_history_file():
    """Display the contents of history.json"""
    print("\n" + "="*60)
    print("HISTORY FILE CONTENTS (history.json)")
    print("="*60)
    
    if os.path.exists('history.json'):
        with open('history.json', 'r') as f:
            content = f.read()
            print(content)
    else:
        print("No history file found")

def run_all_tests():
    """Run all history manager tests"""
    print("\n" + "#"*60)
    print("# TESTING history_manager.py")
    print("#"*60)
    
    try:
        test_initialization()
        test_add_entry()
        test_get_history()
        test_persistence()
        test_clear_history()
        test_corrupt_file_handling()
        
        display_history_file()
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*60)
        print("\nGenerated Files:")
        print("  - history.json (history log file)")
        
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