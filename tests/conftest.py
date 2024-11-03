"""Common test configuration and fixtures."""

import pytest
import logging
import os
from pathlib import Path

# Configure logging for tests
@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

# Create temporary directory for test files
@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

# Mock cookie data
@pytest.fixture
def mock_cookie_data():
    return {
        "sessionId": "test_session",
        "__Host-authjs.csrf-token": "test_csrf",
        "__Secure-authjs.session-token": "test_token"
    }

# Test paths
TEST_DIR = Path(__file__).parent
FIXTURES_DIR = TEST_DIR / "fixtures" 