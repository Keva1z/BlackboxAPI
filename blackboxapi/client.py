import requests
import re
import logging as logging_module
from .models import Message, AgentMode, Chat, Model, BLACKBOX
from .exceptions import APIError
from .utils import load_cookies, parse_and_save_cookies, validate_cookie
from .database import DatabaseInterface, DictDatabase
from typing import Optional
import brotli
import colorama
import aiohttp

colorama.init()

# Define custom logging levels
logging_module.addLevelName(15, 'REQUEST')
logging_module.addLevelName(25, 'RESPONSE')

class LogType:
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'
    DEBUG = 'DEBUG'

class AIClient:
    """
    A client for interacting with the Blackbox AI API.

    Attributes:
        base_url (str): The base URL of the Blackbox AI API.
        headers (dict): The headers to use for the API requests.
        chats (dict): A dictionary of chats, keyed by agent mode ID.
        default_chat (Chat): The default chat.
        logging (bool): Whether to enable logging.
    """

    def __init__(self, base_url="https://www.blackbox.ai", cookie_file: Optional[str] = None, use_chat_history: bool = True, database: Optional[DatabaseInterface] = None, logging: bool = False):
        """
        Initialize the AIClient with the given base URL and cookie file.
        cookie_file: path to the file with cookies
        """

        BROTLI_HOLDER = brotli.MODE_TEXT

        self.base_url = base_url
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.blackbox.ai",
            "priority": "u=1, i",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "YaBrowser";v="24.10", "Yowser";v="2.5"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        
        if cookie_file:
            self.headers["cookie"] = load_cookies(cookie_file)
        else:
            cookie_file = "cookies.json"
            try:
                self.headers["cookie"] = load_cookies(cookie_file)
            except FileNotFoundError:
                while True:
                    cookie_string = input("Please enter the cookie string: ")
                    if validate_cookie(cookie_string):
                        parse_and_save_cookies(cookie_string, cookie_file)
                        self.headers["cookie"] = load_cookies(cookie_file)
                        break
                    else:
                        raise ValueError("Invalid cookie format")
        
        self.use_chat_history = use_chat_history
        self.database = database or DictDatabase()
        
        # Create completions attribute when initializing
        self.completions = Completions(self)

        # Setup logging
        self.enable_logging = logging
        if self.enable_logging:
            self._setup_logging()

        # Create a dictionary mapping log types to logging levels
        self.log_levels = {
            LogType.INFO: logging_module.INFO,
            LogType.WARNING: logging_module.WARNING,
            LogType.ERROR: logging_module.ERROR,
            LogType.REQUEST: 15,  # Custom level for REQUEST
            LogType.RESPONSE: 25,  # Custom level for RESPONSE
            LogType.DEBUG: logging_module.DEBUG
        }

    def _setup_logging(self):
        self.logger = logging_module.getLogger('AIClient')
        self.logger.setLevel(logging_module.DEBUG)
        handler = logging_module.StreamHandler()
        formatter = logging_module.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _log(self, message, log_type=LogType.INFO):
        if self.enable_logging:
            colors = {
                LogType.INFO: colorama.Fore.CYAN,
                LogType.WARNING: colorama.Fore.YELLOW,
                LogType.ERROR: colorama.Fore.RED,
                LogType.REQUEST: colorama.Fore.MAGENTA,
                LogType.RESPONSE: colorama.Fore.GREEN,
                LogType.DEBUG: colorama.Fore.BLUE
            }
            color = colors.get(log_type, colorama.Fore.RESET)
            log_level = self.log_levels.get(log_type, logging_module.INFO)
            self.logger.log(log_level, f"{color}{message}{colorama.Fore.RESET}")

    def _get_chat(self, agent_mode: Optional[AgentMode] = None) -> Chat:
        if not self.use_chat_history:
            return Chat(self.database)
        chat_id = agent_mode.id if agent_mode else "default"
        self._log(f"Getting chat for agent mode: {chat_id}", LogType.DEBUG)
        return self.database.get_or_create_chat(chat_id)

    def _process_response(self, response_text: str) -> str:
        """
        Processes the API response, removing unnecessary links.
        """
        self._log("Processing API response", LogType.DEBUG)
        # Remove the block of links between $~~~$
        cleaned_text = re.sub(r'\$~~~\$.*?\$~~~\$', '', response_text, flags=re.DOTALL)
        
        return cleaned_text

    def _prepare_payload(self, message: str, agent: Optional[AgentMode], model: Model, max_tokens: int) -> tuple[dict, Chat]:
        chat = self._get_chat(agent)
        chat.add_message(message, "user")
        
        payload = {
            "messages": [m.to_dict() for m in chat.get_messages()],
            "id": chat.chat_id,
            "previewToken": None,
            "userId": None,
            "codeModelMode": True,
            "agentMode": agent.to_dict() if agent else {},
            "trendingAgentMode": {},
            "isMicMode": False,
            "maxTokens": max_tokens,
            "playgroundTopP": None,
            "playgroundTemperature": None,
            "isChromeExt": False,
            "githubToken": None,
            "clickedAnswer2": False,
            "clickedAnswer3": False,
            "clickedForceWebSearch": False,
            "visitFromDelta": False,
            "mobileClient": False,
            "userSelectedModel": None if (model == BLACKBOX or agent) else model.id
        }
        
        if agent:
            self.headers["referer"] = f"https://www.blackbox.ai/agent/{agent.id}"
        else:
            self.headers["referer"] = "https://www.blackbox.ai/chat"
        
        return payload, chat

    def _generate(self, message: str, agent: AgentMode|None = None, model: Model = BLACKBOX, max_tokens=1024) -> str:
        self._log(f"Generating response for message: {message[:50]}...", LogType.INFO)
        url = f"{self.base_url}/api/chat"

        payload, chat = self._prepare_payload(message, agent, model, max_tokens)

        self._log(f"Sending request to {url}", LogType.REQUEST)
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            self._log(f"API returned status code {response.status_code}", LogType.ERROR)
            raise APIError(f"API returned status code {response.status_code}: {response.content}")

        try:
            response_text = response.content.decode('utf-8')
            response_text = ''.join(char for char in response_text if char.isprintable() or char == '\n')
            
            processed_response = self._process_response(response_text)
            
            chat.add_message(processed_response, "assistant")
            self._log("Response generated and added to chat history", LogType.RESPONSE)
            return processed_response
        except Exception as e:
            self._log(f"Failed to process the server response: {str(e)}", LogType.ERROR)
            raise APIError("Failed to process the server response")

    async def _generate_async(self, message: str, agent: Optional[AgentMode] = None, model: Model = BLACKBOX, max_tokens: int = 1024) -> str:
        self._log(f"Asynchronously generating response for message: {message[:50]}...", LogType.INFO)
        url = f"{self.base_url}/api/chat"

        payload, chat = self._prepare_payload(message, agent, model, max_tokens)

        self._log(f"Sending async request to {url}", LogType.REQUEST)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status != 200:
                    self._log(f"API returned status code {response.status}", LogType.ERROR)
                    raise APIError(f"API returned status code {response.status}: {await response.text()}")

                try:
                    response_text = await response.text()
                    response_text = ''.join(char for char in response_text if char.isprintable() or char == '\n')
                    
                    processed_response = self._process_response(response_text)
                    
                    chat.add_message(processed_response, "assistant")
                    self._log("Response generated and added to chat history", LogType.RESPONSE)
                    return processed_response
                except Exception as e:
                    self._log(f"Failed to process the server response: {str(e)}", LogType.ERROR)
                    raise APIError("Failed to process the server response")

    def get_chat_history(self, agent: AgentMode|None = None):
        """
        Get the chat history for the given agent mode.
        agent: AgentMode | None = None
        """
        self._log(f"Getting chat history for agent: {agent.id if agent else 'default'}", LogType.INFO)
        chat = self._get_chat(agent)
        return chat.get_messages()

    def clear_chat_history(self, agent: AgentMode|None = None):
        """
        Clear the chat history for the given agent mode.
        agent: AgentMode | None = None
        """
        self._log(f"Clearing chat history for agent: {agent.id if agent else 'default'}", LogType.INFO)
        chat = self._get_chat(agent)
        chat.clear_history()
        self.database.save_chat(chat)

    def delete_chat(self, agent: AgentMode|None = None):
        """
        Delete the chat for the given agent mode.
        agent: AgentMode | None = None
        """
        chat_id = agent.id if agent else "default"
        self._log(f"Deleting chat for agent: {chat_id}", LogType.INFO)
        self.database.delete_chat(chat_id)

class Completions:
    def __init__(self, client: AIClient):
        self.client = client

    def create(self, message: str, agent: Optional[AgentMode] = None, model: Model = BLACKBOX, max_tokens: int = 1024) -> str:
        return self.client._generate(message, agent, model, max_tokens)

    async def create_async(self, message: str, agent: Optional[AgentMode] = None, model: Model = BLACKBOX, max_tokens: int = 1024) -> str:
        return await self.client._generate_async(message, agent, model, max_tokens)

