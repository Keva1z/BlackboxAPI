"""Tests for model and agent implementations."""

import pytest
from blackboxapi.models import (
    Message,
    Chat,
    Model,
    AgentMode
)
from blackboxapi import (
    CLAUDE,
    RU_CAN_CODER,
    DictDatabase
)

def test_message_creation():
    """Test message object creation and properties."""
    msg = Message("Test content", "user")
    assert msg.content == "Test content"
    assert msg.role == "user"
    assert msg.timestamp is not None

def test_chat_operations():
    """Test chat operations and message management."""
    db = DictDatabase()
    chat = Chat(db, "test_chat")
    
    chat.add_message("User message", "user")
    chat.add_message("Assistant message", "assistant")
    
    messages = chat.get_messages()
    assert len(messages) == 2
    assert messages[0].content == "User message"
    assert messages[1].role == "assistant"

def test_model_properties():
    """Test AI model properties."""
    assert CLAUDE.max_tokens == 8192
    assert CLAUDE.supports_streaming is False
    assert CLAUDE.name == "Claude"

def test_agent_mode():
    """Test agent mode properties and behavior."""
    assert RU_CAN_CODER.mode is True
    assert "coding" in RU_CAN_CODER.description.lower()
    assert RU_CAN_CODER.name == "CAN Coder" 