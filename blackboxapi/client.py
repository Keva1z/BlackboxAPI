"""
BlackboxAPI Client Module

This module provides the main client interface for interacting with the Blackbox AI API.
It handles authentication, request management, chat history, and different AI models.
"""

import asyncio
import requests
import re
import logging
import aiohttp
import brotli
import colorama
import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from .models import Message, AgentMode, Chat, Model, BLACKBOX
from .exceptions import APIError
from .utils import load_cookies, parse_and_save_cookies, validate_cookie
from .database import DatabaseInterface, DictDatabase

from blackboxapi.utils import image_to_base64

# Initialize colorama for cross-platform colored output
colorama.init()

# Configure module logger
logger = logging.getLogger(__name__)

# Custom logging levels for request tracking
logging.addLevelName(15, 'REQUEST')
logging.addLevelName(25, 'RESPONSE')

class LogType:
    """Constants for different types of log messages."""
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'
    DEBUG = 'DEBUG'

class BaseAIClient(ABC):
    """Base abstract class for AI clients.
    
    Defines common functionality and interface for both sync and async clients.
    """
    
    _last_validated_value = None
    _validated_cache_file = "validated_cache.json"
    _validated_cache_ttl = timedelta(hours=4)
    
    def __init__(
        self,
        base_url: str = "https://www.blackbox.ai",
        cookie_file: Optional[str] = None,
        use_chat_history: bool = True,
        database: Optional[DatabaseInterface] = None,
        enable_logging: bool = False
    ):
        """Initialize the base client."""
        self.base_url = base_url
        self.use_chat_history = use_chat_history
        self.database = database or DictDatabase()
        self.enable_logging = enable_logging
        
        self.headers = self._initialize_headers()
        self._setup_authentication(cookie_file)
        
        if self.enable_logging:
            self._setup_logging()

        self.log_levels = {
            LogType.INFO: logging.INFO,
            LogType.WARNING: logging.WARNING,
            LogType.ERROR: logging.ERROR,
            LogType.REQUEST: 15,
            LogType.RESPONSE: 25,
            LogType.DEBUG: logging.DEBUG
        }

        self._load_validated_from_cache()

    def _initialize_headers(self) -> Dict[str, str]:
        """Initialize default HTTP headers for requests."""
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.blackbox.ai",
            "priority": "u=1, i",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }

    def _setup_authentication(self, cookie_file: Optional[str]) -> None:
        """Set up authentication using cookies.
        
        Args:
            cookie_file (Optional[str]): Path to cookie file
            
        Raises:
            ValueError: If cookie validation fails
        """
        if cookie_file:
            self.headers["cookie"] = load_cookies(cookie_file)
        else:
            cookie_file = "cookies.json"
            try:
                self.headers["cookie"] = load_cookies(cookie_file)
            except FileNotFoundError:
                self._handle_missing_cookies(cookie_file)

    def _handle_missing_cookies(self, cookie_file: str) -> None:
        """Handle the case when cookie file is missing.
        
        Args:
            cookie_file (str): Path where to save cookies
            
        Raises:
            ValueError: If provided cookie string is invalid
        """
        while True:
            cookie_string = input("Please enter the cookie string: ")
            if validate_cookie(cookie_string):
                parse_and_save_cookies(cookie_string, cookie_file)
                self.headers["cookie"] = load_cookies(cookie_file)
                break
            else:
                raise ValueError("Invalid cookie format")

    def _setup_logging(self) -> None:
        """Configure logging for the client."""
        self.logger = logging.getLogger('AIClient')
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _log(self, message: str, log_type: str = LogType.INFO) -> None:
        """Log a message with the specified type and color.
        
        Args:
            message (str): The message to log
            log_type (str): Type of log message
        """
        if not self.enable_logging:
            return
            
        colors = {
            LogType.INFO: colorama.Fore.CYAN,
            LogType.WARNING: colorama.Fore.YELLOW,
            LogType.ERROR: colorama.Fore.RED,
            LogType.REQUEST: colorama.Fore.MAGENTA,
            LogType.RESPONSE: colorama.Fore.GREEN,
            LogType.DEBUG: colorama.Fore.BLUE
        }
        
        color = colors.get(log_type, colorama.Fore.RESET)
        log_level = self.log_levels.get(log_type, logging.INFO)
        self.logger.log(
            log_level, 
            f"{color}{message}{colorama.Fore.RESET}"
        )

    def _get_chat(self, agent_mode: Optional[AgentMode] = None) -> Chat:
        """Get or create a chat session synchronously.
        
        Args:
            agent_mode (Optional[AgentMode]): The agent mode to get chat for
            
        Returns:
            Chat: The chat session
        """
        if not self.use_chat_history:
            return Chat(self.database)
            
        chat_id = agent_mode.id if agent_mode else "default"
        self._log(f"Getting chat for agent mode: {chat_id}", LogType.DEBUG)
        return self.database.get_or_create_chat(chat_id)

    async def _get_chat_async(self, agent_mode: Optional[AgentMode] = None) -> Chat:
        """Get or create a chat session asynchronously.
        
        Args:
            agent_mode (Optional[AgentMode]): The agent mode to get chat for
            
        Returns:
            Chat: The chat session
        """
        if not self.use_chat_history:
            return Chat(self.database)
            
        chat_id = agent_mode.id if agent_mode else "default"
        self._log(f"Getting chat for agent mode: {chat_id}", LogType.DEBUG)
        return await self.database.get_or_create_chat_async(chat_id)

    def _process_response(self, response_text: str) -> str:
        """Process and clean the API response text.
        
        Args:
            response_text (str): Raw response text
            
        Returns:
            str: Cleaned response text
        """
        self._log("Processing API response", LogType.DEBUG)
        # Удаляем специальные маркеры
        cleaned_text = re.sub(r'\$~~~\$.*?\$~~~\$', '', response_text, flags=re.DOTALL)
        cleaned_text = re.sub(r'Generated by BLACKBOX\.AI, try unlimited chat https://www\.blackbox\.ai\n\n?', '', cleaned_text)
        return cleaned_text

    def _load_validated_from_cache(self) -> None:
        """Load validated value from cache file if it exists and is not expired."""
        try:
            if os.path.exists(self._validated_cache_file):
                with open(self._validated_cache_file, 'r') as f:
                    cache_data = json.load(f)
                    cached_time = datetime.fromisoformat(cache_data['timestamp'])
                    if datetime.utcnow() - cached_time < self._validated_cache_ttl:
                        self._last_validated_value = cache_data['value']
                        self._log(f"Loaded validated value from cache: {self._last_validated_value}", LogType.DEBUG)
        except Exception as e:
            self._log(f"Failed to load validated cache: {str(e)}", LogType.ERROR)

    def _save_validated_to_cache(self, value: str) -> None:
        """Save validated value to cache file."""
        try:
            cache_data = {
                'value': value,
                'timestamp': datetime.utcnow().isoformat()
            }
            with open(self._validated_cache_file, 'w') as f:
                json.dump(cache_data, f)
            self._log("Saved validated value to cache", LogType.DEBUG)
        except Exception as e:
            self._log(f"Failed to save validated cache: {str(e)}", LogType.ERROR)

    async def _fetch_validated(self) -> str:
        """Fetch validated value from Blackbox website JS files.
        
        Returns:
            str: Validated value for API requests
        """
        # Проверяем кэш в памяти
        if self._last_validated_value:
            return self._last_validated_value

        # Пытаемся получить новое значение
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.base_url) as response:
                    if response.status != 200:
                        logger.error("Failed to load the main page")
                        return self._last_validated_value
                    
                    page_content = await response.text()
                    js_files = re.findall(r'static/chunks/\d{4}-[a-fA-F0-9]+\.js', page_content)

                key_pattern = re.compile(r'w="([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"')

                for js_file in js_files:
                    js_url = f"{self.base_url}/_next/{js_file}"
                    async with session.get(js_url) as js_response:
                        if js_response.status == 200:
                            js_content = await js_response.text()
                            match = key_pattern.search(js_content)
                            if match:
                                validated_value = match.group(1)
                                self._last_validated_value = validated_value
                                # Сохраняем новое значение в кэш
                                self._save_validated_to_cache(validated_value)
                                return validated_value
                                
            except Exception as e:
                logger.error(f"Error fetching validated value: {str(e)}")

        return self._last_validated_value

    async def _prepare_payload_async(
        self, 
        message: str, 
        agent: Optional[AgentMode],
        model: Model, 
        max_tokens: int,
        image: Optional[str] = None
    ) -> tuple[dict, Chat]:
        """Prepare the request payload and chat session asynchronously."""
        chat = await self._get_chat_async(agent)
        await chat.add_message_async(message + "\n\nОтвечай только на том языке, на котором я задал вопрос. Т.е задал на русском - ответил на русском.", "user", image)
        
        validated_value = await self._fetch_validated()
        
        payload = {
            "messages": [m.to_dict() for m in await chat.get_messages_async()],
            "id": chat.chat_id,
            "previewToken": None,
            "userId": None,
            "codeModelMode": True,
            "agentMode": agent.to_dict() if agent else {},
            "trendingAgentMode": {},
            "isMicMode": False,
            "userSystemPrompt": None,
            "maxTokens": max_tokens,
            "playgroundTopP": 0.9,
            "playgroundTemperature": 0.5,
            "isChromeExt": False,
            "githubToken": None,
            "clickedAnswer2": False,
            "clickedAnswer3": False,
            "clickedForceWebSearch": False,
            "visitFromDelta": False,
            "mobileClient": False,
            "userSelectedModel": None,
            "validated": validated_value
        }

        # Если нет изображения и не используется агент или BLACKBOX модель,
        # устанавливаем выбранную модель
        if image is None and not agent and model != BLACKBOX:
            payload["userSelectedModel"] = model.id
        
        # Update referer header based on agent mode
        self.headers["referer"] = (
            f"https://www.blackbox.ai/agent/{agent.id}"
            if agent else
            "https://www.blackbox.ai/chat"
        )
        
        return payload, chat

    def _prepare_payload(
        self, 
        message: str, 
        agent: Optional[AgentMode],
        model: Model, 
        max_tokens: int,
        image: Optional[str] = None
    ) -> tuple[dict, Chat]:
        """Prepare the request payload and chat session synchronously."""
        chat = self._get_chat(agent)
        chat.add_message(message + "\n\nОтвечай только на том языке, на котором я задал вопрос. Т.е задал на русском - ответил на русском.", "user", image)
        
        # For sync client, we still need to run fetch_validated in an event loop
        validated_value = asyncio.run(self._fetch_validated())
        
        payload = {
            "messages": [m.to_dict() for m in chat.get_messages()],
            "id": chat.chat_id,
            "previewToken": None,
            "userId": None,
            "codeModelMode": True,
            "agentMode": agent.to_dict() if agent else {},
            "trendingAgentMode": {},
            "isMicMode": False,
            "userSystemPrompt": None,
            "maxTokens": max_tokens,
            "playgroundTopP": 0.9,
            "playgroundTemperature": 0.5,
            "isChromeExt": False,
            "githubToken": None,
            "clickedAnswer2": False,
            "clickedAnswer3": False,
            "clickedForceWebSearch": False,
            "visitFromDelta": False,
            "mobileClient": False,
            "userSelectedModel": None,
            "validated": validated_value
        }

        # Если нет изображения и не используется агент или BLACKBOX модель,
        # устанавливаем выбранную модель
        if image is None and not agent and model != BLACKBOX:
            payload["userSelectedModel"] = model.id
        
        # Update referer header based on agent mode
        self.headers["referer"] = (
            f"https://www.blackbox.ai/agent/{agent.id}"
            if agent else
            "https://www.blackbox.ai/chat"
        )
        
        return payload, chat

    @abstractmethod
    def _generate(self, message: str, agent: Optional[AgentMode], model: Model, 
                 max_tokens: int, image: Optional[str]) -> str:
        """Abstract method for synchronous generation."""
        pass

    @abstractmethod
    async def _generate_async(self, message: str, agent: Optional[AgentMode], 
                            model: Model, max_tokens: int, image: Optional[str]) -> str:
        """Abstract method for asynchronous generation."""
        pass

class AsyncCompletions:
    """Async completions handler."""
    
    def __init__(self, client: 'AsyncAIClient'):
        self.client = client

    async def create(
        self, 
        message: str, 
        agent: Optional[AgentMode] = None, 
        model: Model = BLACKBOX, 
        max_tokens: int = 1024,
        image: Optional[str] = None
    ) -> str:
        """Generate completion asynchronously."""
        return await self.client._generate_async(message, agent, model, max_tokens, image)

class SyncCompletions:
    """Sync completions handler."""
    
    def __init__(self, client: 'AIClient'):
        self.client = client

    def create(
        self, 
        message: str, 
        agent: Optional[AgentMode] = None, 
        model: Model = BLACKBOX, 
        max_tokens: int = 1024,
        image: Optional[str] = None
    ) -> str:
        """Generate completion synchronously."""
        return self.client._generate(message, agent, model, max_tokens, image)

class AsyncAIClient(BaseAIClient):
    """Asynchronous AI client implementation."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completions = AsyncCompletions(self)

    def _generate(self, message: str, agent: Optional[AgentMode], model: Model, 
                 max_tokens: int, image: Optional[str]) -> str:
        """Sync generation not supported in async client."""
        raise NotImplementedError("Use create() for async generation")

    async def _generate_async(self, message: str, agent: Optional[AgentMode], 
                            model: Model, max_tokens: int, image: Optional[str]) -> str:
        """Async generation implementation."""
        url = f"{self.base_url}/api/chat"
        if image is not None: 
            image = image_to_base64(image)
        payload, chat = await self._prepare_payload_async(message, agent, model, max_tokens, image)

        self._log(f"Sending async request to {url}", LogType.REQUEST)
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    self._log(f"API returned status code {response.status}", LogType.ERROR)
                    raise APIError(f"API returned status code {response.status}: {await response.text()}")

                try:
                    response_text = await response.text()
                    processed_response = self._process_response(response_text)
                    await chat.add_message_async(processed_response, "assistant")
                    self._log("Response generated and added to chat history", LogType.RESPONSE)
                    return processed_response
                    
                except Exception as e:
                    self._log(f"Failed to process the server response: {str(e)}", LogType.ERROR)
                    raise APIError("Failed to process the server response")

    async def get_chat_history(self, agent: Optional[AgentMode] = None) -> List[Message]:
        """Get chat history asynchronously."""
        chat = await self._get_chat_async(agent)
        return await chat.get_messages_async()

    async def clear_chat_history(self, agent: Optional[AgentMode] = None) -> None:
        """Clear chat history asynchronously."""
        chat = await self._get_chat_async(agent)
        await chat.clear_history_async()
        await self.database.save_chat_async(chat)

    async def delete_chat(self, agent: Optional[AgentMode] = None) -> None:
        """Delete chat asynchronously."""
        chat_id = agent.id if agent else "default"
        await self.database.delete_chat_async(chat_id)

class AIClient(BaseAIClient):
    """Synchronous AI client implementation."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completions = SyncCompletions(self)

    async def _generate_async(self, message: str, agent: Optional[AgentMode], 
                            model: Model, max_tokens: int, image: Optional[str]) -> str:
        """Async generation not supported in sync client."""
        raise NotImplementedError("Use create() for sync generation")

    def _generate(self, message: str, agent: Optional[AgentMode], model: Model, 
                 max_tokens: int, image: Optional[str]) -> str:
        """Sync generation implementation."""
        url = f"{self.base_url}/api/chat"
        if image is not None:
            image = image_to_base64(image)
        payload, chat = self._prepare_payload(message, agent, model, max_tokens, image)

        self._log(f"Sending request to {url}", LogType.REQUEST)
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            self._log(f"API returned status code {response.status_code}", LogType.ERROR)
            raise APIError(f"API returned status code {response.status_code}: {response.content}")

        try:
            response_text = response.content.decode('utf-8')
            processed_response = self._process_response(response_text)
            chat.add_message(processed_response, "assistant")
            self._log("Response generated and added to chat history", LogType.RESPONSE)
            return processed_response
            
        except Exception as e:
            self._log(f"Failed to process the server response: {str(e)}", LogType.ERROR)
            raise APIError("Failed to process the server response")

