"""Tests for database implementations."""

import pytest
from blackboxapi import (
    DatabaseInterface,
    DictDatabase,
    Chat,
    DatabaseError
)
from datetime import datetime

@pytest.fixture
def db():
    """Create a fresh database instance for each test."""
    return DictDatabase()

def test_dict_database_basic_operations(db):
    """Test basic CRUD operations."""
    # Create
    chat = db.get_or_create_chat("test_chat")
    assert chat.chat_id == "test_chat"
    
    # Read
    retrieved = db.get_chat("test_chat")
    assert retrieved is not None
    assert retrieved.chat_id == "test_chat"
    
    # Update
    chat.add_message("Test message", "user")
    db.save_chat(chat)
    updated = db.get_chat("test_chat")
    assert len(updated.get_messages()) == 1
    
    # Delete
    db.delete_chat("test_chat")
    assert db.get_chat("test_chat") is None

def test_metadata_tracking(db):
    """Test metadata management."""
    chat = db.get_or_create_chat("test_chat")
    metadata = db.get_chat_metadata("test_chat")
    
    assert metadata is not None
    assert "created_at" in metadata
    assert "message_count" in metadata
    assert metadata["message_count"] == 0
    
    chat.add_message("Test", "user")
    db.save_chat(chat)
    
    updated_metadata = db.get_chat_metadata("test_chat")
    assert updated_metadata["message_count"] == 1 