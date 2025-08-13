"""
Configuration for acceptance tests.
"""
import pytest
import os
from support.app_driver import check_server_health


def pytest_configure(config):
    """Configure pytest for acceptance tests."""
    # Only check server if not explicitly skipped
    skip_server_check = os.environ.get('SKIP_SERVER_CHECK', '').lower() in ('true', '1', 'yes')
    
    if not skip_server_check:
        # Ensure the server is running before starting tests
        if not check_server_health():
            pytest.exit("Application server is not running. Please start it with 'pnpm dev'")


@pytest.fixture(scope="session", autouse=True)
def ensure_server_running():
    """Ensure the server is running for the test session."""
    skip_server_check = os.environ.get('SKIP_SERVER_CHECK', '').lower() in ('true', '1', 'yes')
    
    if not skip_server_check and not check_server_health():
        pytest.skip("Application server is not running")