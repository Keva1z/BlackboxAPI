"""
Utility functions for cookie management and other helper operations
in the BlackboxAPI library.
"""

import json
import os
import re
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def load_cookies(file_path: str) -> str:
    """Load cookies from a file and format them for use in HTTP headers.
    
    Args:
        file_path (str): Path to the cookie file (JSON format)
        
    Returns:
        str: Formatted cookie string
        
    Raises:
        FileNotFoundError: If the cookie file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    logger.debug(f"Loading cookies from: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"Cookie file not found: {file_path}")
        raise FileNotFoundError(f"File with cookies not found: {file_path}")
    
    with open(file_path, 'r') as file:
        try:
            cookies = json.load(file)
            cookie_string = '; '.join(f"{key}={value}" for key, value in cookies.items())
            logger.debug("Successfully loaded cookies")
            return cookie_string
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON, trying as raw string: {str(e)}")
            return file.read().strip()

def parse_and_save_cookies(cookie_string: str, file_path: str) -> Dict[str, str]:
    """Parse a cookie string and save it to a JSON file.
    
    Args:
        cookie_string (str): Raw cookie string from browser
        file_path (str): Path where to save the parsed cookies
        
    Returns:
        Dict[str, str]: Dictionary of parsed cookies
        
    Raises:
        ValueError: If the cookie string is invalid
    """
    logger.debug("Parsing and saving cookies")
    
    try:
        cookie_dict = dict(
            item.split('=', 1) 
            for item in re.split(r';\s*', cookie_string) 
            if '=' in item
        )
        
        cookie_data = {
            "cookies": cookie_dict,
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "last_modified": datetime.utcnow().isoformat()
            }
        }

        with open(file_path, 'w') as file:
            json.dump(cookie_data, file, indent=2)
            
        logger.info(f"Saved cookies to: {file_path}")
        return cookie_dict
        
    except Exception as e:
        logger.error(f"Failed to parse and save cookies: {str(e)}")
        raise ValueError(f"Failed to process cookie string: {str(e)}")

def validate_cookie(cookie_string: str) -> bool:
    """Validate a cookie string for required authentication fields.
    
    Args:
        cookie_string (str): The cookie string to validate
        
    Returns:
        bool: True if the cookie contains all required fields
    """
    required_fields = {
        'sessionId',
        '__Host-authjs.csrf-token',
        '__Secure-authjs.session-token'
    }
    
    try:
        cookie_dict = dict(
            item.split('=', 1) 
            for item in re.split(r';\s*', cookie_string) 
            if '=' in item
        )
        
        is_valid = required_fields.issubset(cookie_dict.keys())
        logger.debug(f"Cookie validation {'successful' if is_valid else 'failed'}")
        return is_valid
        
    except Exception as e:
        logger.error(f"Cookie validation error: {str(e)}")
        return False

def get_cookie_expiration(cookie_dict: Dict[str, str]) -> Optional[datetime]:
    """Get the expiration date of the session cookie.
    
    Args:
        cookie_dict (Dict[str, str]): Dictionary of cookies
        
    Returns:
        Optional[datetime]: Expiration datetime if found, None otherwise
    """
    try:
        if 'expires' in cookie_dict:
            return datetime.strptime(cookie_dict['expires'], '%a, %d-%b-%Y %H:%M:%S GMT')
        return None
    except Exception as e:
        logger.error(f"Failed to parse cookie expiration: {str(e)}")
        return None
