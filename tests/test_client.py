"""Tests for the AIClient class and its functionality."""

import pytest
from unittest.mock import Mock, patch
from blackboxapi import (
    AIClient, 
    RU_CAN_CODER,
    CLAUDE,
    APIError,
    DatabaseError
)

@pytest.fixture
def client():
    """Create a test client with mock cookies."""
    with patch('blackboxapi.client.load_cookies') as mock_load:
        mock_load.return_value = "test_cookie"
        return AIClient(cookie_file="test_cookies.json")

def test_client_initialization(client):
    """Test client initialization with default parameters."""
    assert client.base_url == "https://www.blackbox.ai"
    assert client.use_chat_history is True
    assert client.logging is False

@pytest.mark.asyncio
async def test_async_completion(client):
    """Test asynchronous completion generation."""
    with patch('blackboxapi.client.AIClient._make_async_request') as mock_request:
        mock_request.return_value = {"response": "Test response"}
        response = await client.completions.create_async(
            "Test message",
            agent=RU_CAN_CODER,
            model=CLAUDE
        )
        assert response == "Test response"

def test_chat_history_management(client):
    """Test chat history operations."""
    client.completions.create("Test message 1")
    client.completions.create("Test message 2")
    
    history = client.get_chat_history()
    assert len(history) == 2
    assert history[0].content == "Test message 1"
    
    client.clear_chat_history()
    assert len(client.get_chat_history()) == 0
