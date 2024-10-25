import json
import os
import re

def load_cookies(file_path):
    """
    Load cookies from a file.

    Args:
        file_path (str): Path to the cookie file.

    Returns:
        str: Cookie string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File with cookies not found: {file_path}")
    
    with open(file_path, 'r') as file:
        try:
            cookies = json.load(file)
            return '; '.join([f"{key}={value}" for key, value in cookies.items()])
        except json.JSONDecodeError:
            file.seek(0)
            return file.read().strip()

def parse_and_save_cookies(cookie_string, file_path):
    """
    Parse a cookie string and save it to a file.

    Args:
        cookie_string (str): The cookie string to parse.
        file_path (str): Path to save the parsed cookies.

    Returns:
        dict: Parsed cookies as a dictionary.
    """
    cookie_dict = {}
    for item in re.split(r';\s*', cookie_string):
        if '=' in item:
            key, value = item.split('=', 1)
            cookie_dict[key.strip()] = value.strip()

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump(cookie_dict, file, indent=2)
        print(f"File with cookies created: {file_path}")
    else:
        print(f"File with cookies already exists: {file_path}")

    return cookie_dict

def validate_cookie(cookie_string):
    """
    Validate a cookie string.

    Args:
        cookie_string (str): The cookie string to validate.

    Returns:
        bool: True if the cookie is valid, False otherwise.
    """
    required_fields = ['sessionId', '__Host-authjs.csrf-token', '__Secure-authjs.session-token']
    
    cookie_dict = {}
    for item in re.split(r';\s*', cookie_string):
        if '=' in item:
            key, value = item.split('=', 1)
            cookie_dict[key.strip()] = value.strip()
    
    for field in required_fields:
        if field not in cookie_dict:
            return False
    
    return True
