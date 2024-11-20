"""
BlackboxAPI - Python Library for Blackbox AI Integration

This library provides a clean interface for interacting with the Blackbox AI API,
supporting multiple AI models, agent modes, and both synchronous and asynchronous operations.

Basic usage:
    from blackboxapi import AIClient, RU_CAN_CODER
    
    client = AIClient()
    response = client.completions.create(
        "How do I create a REST API?",
        agent=RU_CAN_CODER
    )
    print(response)

For more information, visit: https://github.com/Keva1z/blackboxapi
"""

__version__ = "0.5.0"
__author__ = "Keva1z"
__email__ = "Keva1z@yandex.ru"
__license__ = "MIT"
__copyright__ = "Copyright 2024 Keva1z"

import logging
from typing import List, Dict

# Configure package-level logger
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Import main components for easy access
from .client import AIClient
from .models import (
    Message,
    AgentMode,
    Chat,
    Model,
    GPT4,
    CLAUDE,
    GEMINI,
    BLACKBOX
)
from .agent import (
    PROMPT_GENERATOR,
    RU_CAN_CODER,
    RU_RELATIONSHIP_COACH,
    RU_MENTAL_ADVISOR,
    RU_ALGORITHM_EXPLAINER,
    RU_IT_EXPERT,
    RU_MATH_TEACHER,
    RU_MATH_EXPERT,
    AVAILABLE_AGENTS,
    get_agent_by_id,
    get_agent_by_name
)
from .exceptions import APIError, DatabaseError
from .database import DatabaseInterface, DictDatabase

# Package metadata
PACKAGE_METADATA = {
    "name": "blackboxapi",
    "version": __version__,
    "author": __author__,
    "email": __email__,
    "license": __license__,
    "copyright": __copyright__,
    "repository": "https://github.com/Keva1z/blackboxapi",
    "documentation": "https://github.com/Keva1z/blackboxapi/tree/main/examples",
    "description": "Python library for Blackbox AI API integration"
}

# Available models
AVAILABLE_MODELS: List[Model] = [
    GPT4,
    CLAUDE,
    GEMINI,
    BLACKBOX
]

# Model capabilities
MODEL_CAPABILITIES: Dict[str, Dict] = {
    "GPT4": {
        "max_tokens": 8192,
        "supports_streaming": False,
        "languages": ["en", "ru", "many others"],
        "specialties": ["general", "coding", "analysis"]
    },
    "CLAUDE": {
        "max_tokens": 8192,
        "supports_streaming": False,
        "languages": ["en", "ru", "many others"],
        "specialties": ["general", "analysis", "writing"]
    },
    "GEMINI": {
        "max_tokens": 4096,
        "supports_streaming": False,
        "languages": ["en", "ru", "many others"],
        "specialties": ["general", "coding", "math"]
    },
    "BLACKBOX": {
        "max_tokens": 2048,
        "supports_streaming": False,
        "languages": ["en", "ru"],
        "specialties": ["general", "coding"]
    }
}

__all__ = [
    # Main client
    'AIClient',
    
    # Models and core classes
    'Message',
    'AgentMode',
    'Chat',
    'Model',
    
    # Available models
    'GPT4',
    'CLAUDE',
    'GEMINI',
    'BLACKBOX',
    'AVAILABLE_MODELS',
    'MODEL_CAPABILITIES',
    
    # Agent modes
    'PROMPT_GENERATOR',
    'RU_CAN_CODER',
    'RU_RELATIONSHIP_COACH',
    'RU_MENTAL_ADVISOR',
    'RU_ALGORITHM_EXPLAINER',
    'RU_IT_EXPERT',
    'RU_MATH_TEACHER',
    'RU_MATH_EXPERT',
    'AVAILABLE_AGENTS',
    
    # Helper functions
    'get_agent_by_id',
    'get_agent_by_name',
    
    # Database interfaces
    'DatabaseInterface',
    'DictDatabase',
    
    # Exceptions
    'APIError',
    'DatabaseError',
    
    # Package metadata
    'PACKAGE_METADATA'
]
