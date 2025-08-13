#!/usr/bin/env python3
"""
Test runner for acceptance tests.

This script runs the pytest-bdd acceptance tests for the AI chatbot application.
It ensures the application server is running and executes the BDD scenarios.
"""

import sys
import subprocess
import time
import requests
import argparse
import os
from pathlib import Path


def check_server_running(base_url="http://localhost:3000", timeout=30):
    """Check if the application server is running."""
    print(f"Checking if server is running at {base_url}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/ping", timeout=5)
            if response.status_code == 200:
                print("✓ Server is running")
                return True
        except requests.RequestException:
            pass
        time.sleep(2)
    
    print("✗ Server is not running")
    return False


def run_tests(test_pattern=None, markers=None, verbose=False, skip_server_check=False):
    """Run the acceptance tests."""
    cmd = ["python", "-m", "pytest", "tests/acceptance/step_defs/"]
    
    if verbose:
        cmd.append("-v")
    
    if test_pattern:
        cmd.extend(["-k", test_pattern])
    
    if markers:
        cmd.extend(["-m", markers])
    
    # Add other useful options
    cmd.extend([
        "--tb=short",  # Shorter traceback format
        "--maxfail=5",  # Stop after 5 failures
        "--disable-warnings",  # Reduce noise
    ])
    
    # Set environment variable for server check
    env = {}
    if skip_server_check:
        env["SKIP_SERVER_CHECK"] = "true"
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent, env={**subprocess.os.environ, **env})
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run acceptance tests for the AI chatbot")
    parser.add_argument(
        "--pattern", "-k", 
        help="Run tests matching this pattern"
    )
    parser.add_argument(
        "--markers", "-m",
        help="Run tests with specific markers (e.g., 'smoke', 'not skip_unimplemented')"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--skip-server-check",
        action="store_true",
        help="Skip checking if server is running"
    )
    
    args = parser.parse_args()
    
    # Check if server is running unless skipped
    if not args.skip_server_check:
        if not check_server_running():
            print("\nError: Application server is not running.")
            print("Please start it with: pnpm dev")
            print("Or run with --skip-server-check to bypass this check")
            return 1
    
    # Run the tests
    print("\nRunning acceptance tests...")
    return_code = run_tests(
        test_pattern=args.pattern,
        markers=args.markers,
        verbose=args.verbose,
        skip_server_check=args.skip_server_check
    )
    
    if return_code == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ Tests failed with return code {return_code}")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())