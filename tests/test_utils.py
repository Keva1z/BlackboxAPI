"""Tests for utility functions."""

import pytest
import os
import json
from blackboxapi.utils import (
    load_cookies,
    parse_and_save_cookies,
    validate_cookie,
    get_cookie_expiration
)

@pytest.fixture
def cookie_file(tmp_path):
    """Create a temporary cookie file."""
    file_path = tmp_path / "cookies.json"
    cookies = {
        "sessionId": "test_session",
        "__Host-authjs.csrf-token": "test_csrf",
        "__Secure-authjs.session-token": "test_token"
    }
    with open(file_path, 'w') as f:
        json.dump(cookies, f)
    return file_path

def test_cookie_loading(cookie_file):
    """Test loading cookies from file."""
    cookie_string = load_cookies(str(cookie_file))
    assert "sessionId=test_session" in cookie_string
    assert "__Host-authjs.csrf-token=test_csrf" in cookie_string

def test_cookie_validation():
    """Test cookie string validation."""
    valid_cookie = (
        "sessionId=test;"
        "__Host-authjs.csrf-token=test;"
        "__Secure-authjs.session-token=test"
    )
    assert validate_cookie(valid_cookie) is True
    
    invalid_cookie = "sessionId=test"
    assert validate_cookie(invalid_cookie) is False 