"""
Master Test Runner
Runs all module tests in sequence

HOW TO RUN:
    python tests/run_all_tests.py

This will run all tests and generate a complete test report.
"""

import sys
import os
import subprocess

# Change to the tests directory
tests_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(tests_dir)

test_files = [
    'test_models.py',
    'test_history_manager.py',
    'test_image_processing.py',
    'test_controller.py'
]

def run_test(test_file):
    """Run a single test file"""
    print("\n" + "="*70)
    print(f"RUNNING: {test_file}")
    print("="*70)
    
    result = subprocess.run([sys.executable, test_file], capture_output=False)
    return result.returncode == 0

def main():
    print("\n" + "#"*70)
    print("# ASTRO IMAGE COLORIZER - COMPLETE TEST SUITE")
    print("#"*70)
    
    results = {}
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"\n✗ Test file not found: {test_file}")
            results[test_file] = False
            continue
        
        success = run_test(test_file)
        results[test_file] = success
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_file, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {test_file}")
    
    print("\n" + "-"*70)
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print("-"*70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉\n")
        return 0
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED ⚠️\n")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)