import requests
from .models import Message, AgentMode, Chat, Model, BLACKBOX
from .exceptions import APIError
from .utils import load_cookies, parse_and_save_cookies, validate_cookie

class AIClient:
    """
    A client for interacting with the Blackbox AI API.

    Attributes:
        base_url (str): The base URL of the Blackbox AI API.
        headers (dict): The headers to use for the API requests.
        chats (dict): A dictionary of chats, keyed by agent mode ID.
        default_chat (Chat): The default chat.
    """

    def __init__(self, base_url="https://www.blackbox.ai", cookie_file: str|None = None):
        """
        Initialize the AIClient with the given base URL and cookie file.
        cookie_file: path to the file with cookies
        """
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
        
        self.chats = {}
        self.default_chat = Chat()

    def _get_chat(self, agent_mode: AgentMode|None = None):
        """
        Get or create a chat for the given agent mode.
        agent_mode: AgentMode | None = None
        """
        if agent_mode is None:
            return self.default_chat
        return self.chats.setdefault(agent_mode.id, Chat())

    def generate(self, message: str, agent: AgentMode|None = None, model: Model = BLACKBOX, max_tokens=1024) -> str:
        """
        Generate a response from the AI model.

        Args:
            message (str): The input message.
            agent (AgentMode, optional): The agent mode to use.
            model (Model, optional): The AI model to use. Defaults to BLACKBOX.
            max_tokens (int, optional): Maximum number of tokens in the response. Defaults to 1024.

        Returns:
            str: The generated response.
        """
        url = f"{self.base_url}/api/chat"

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

        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise APIError(f"API вернула код состояния {response.status_code}: {response.content}")

        try:
            response_text = response.content.decode('utf-8')
            response_text = ''.join(char for char in response_text if char.isprintable() or char == '\n')
            chat.add_message(response_text, "assistant")
            return response_text
        except Exception as e:
            raise APIError("Failed to process the server's response")

    def get_chat_history(self, agent: AgentMode|None = None):
        """
        Get the chat history for the given agent mode.
        agent: AgentMode | None = None
        """
        return self.get_chat(agent).get_messages()

    def clear_chat_history(self, agent: AgentMode|None = None):
        """
        Clear the chat history for the given agent mode.
        agent: AgentMode | None = None
        """
        self.get_chat(agent).clear_history()
