#!/usr/bin/env python3
"""
Test runner for AI Roast Machine.
Runs all unit tests and reports results.
"""

import os
import sys
import unittest
import argparse
import time

def run_tests(verbose=False, pattern=None):
    """Run all tests in the tests directory.
    
    Args:
        verbose: Whether to show verbose output
        pattern: Pattern to match test files
    
    Returns:
        True if all tests pass, False otherwise
    """
    # Start timer
    start_time = time.time()
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Set test pattern if provided
    if pattern:
        loader.testNamePattern = pattern
    
    # Discover tests
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(tests_dir)
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    
    # Run tests
    result = runner.run(suite)
    
    # Calculate time
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"Test Summary:")
    print(f"  Ran {result.testsRun} tests in {elapsed_time:.2f} seconds")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    # Return True if all tests pass
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Main function."""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run AI Roast Machine tests')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('-p', '--pattern', help='Pattern to match test files')
    args = parser.parse_args()
    
    # Run tests
    success = run_tests(verbose=args.verbose, pattern=args.pattern)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 