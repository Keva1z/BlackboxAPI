"""
Utility functions for cookie management and other helper operations
in the BlackboxAPI library.
"""

import base64
from PIL.Image import Image
from typing import Union, IO
from io import BytesIO
import json
import os
import re
import logging
from typing import Dict, Optional
from datetime import datetime
import requests

ImageType = Union[str, bytes, IO, Image, None]
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

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

def is_accepted_format(binary_data: bytes) -> str:
    """
    Checks if the given binary data represents an image with an accepted format.
    
    Args:
        binary_data (bytes): The binary data to check.
        
    Returns:
        str: MIME type of the image
        
    Raises:
        ValueError: If the image format is not allowed.
    """
    if binary_data.startswith(b'\xFF\xD8\xFF'):
        return "image/jpeg"
    elif binary_data.startswith(b'\x89PNG\r\n\x1a\n'):
        return "image/png"
    elif binary_data.startswith(b'GIF87a') or binary_data.startswith(b'GIF89a'):
        return "image/gif"
    elif binary_data.startswith(b'\x89JFIF') or binary_data.startswith(b'JFIF\x00'):
        return "image/jpeg"
    elif binary_data.startswith(b'\xFF\xD8'):
        return "image/jpeg"
    elif binary_data.startswith(b'RIFF') and binary_data[8:12] == b'WEBP':
        return "image/webp"
    else:
        raise ValueError("Invalid image format (from magic code).")

def to_bytes(image: ImageType) -> bytes:
    """
    Converts the given image to bytes.
    
    Args:
        image (ImageType): The image to convert (can be path, bytes, PIL Image, or file-like object)
        
    Returns:
        bytes: The image as bytes
        
    Raises:
        ValueError: If image format is invalid
    """
    try:
        # Если передан путь к файлу
        if isinstance(image, str) and not image.startswith('data:'):
            with open(image, 'rb') as f:
                return f.read()
                
        # Если передан file-like объект (например response.raw)
        elif hasattr(image, 'read'):
            # Читаем все содержимое потока
            chunks = []
            while True:
                chunk = image.read(8192)  # Читаем по 8KB
                if not chunk:
                    break
                chunks.append(chunk)
            # Восстанавливаем позицию, если возможно
            if hasattr(image, 'seek'):
                try:
                    image.seek(0)
                except (OSError, IOError):
                    pass
            return b''.join(chunks)
            
        # Если переданы байты
        elif isinstance(image, bytes):
            return image
            
        # Если передано PIL Image
        elif isinstance(image, Image):
            bytes_io = BytesIO()
            image.save(bytes_io, format=image.format or 'JPEG')
            return bytes_io.getvalue()
            
        # Если передана data URI строка
        elif isinstance(image, str) and image.startswith('data:'):
            return extract_data_uri(image)
            
        else:
            raise ValueError("Unsupported image type")
            
    except Exception as e:
        logger.error(f"Failed to convert image to bytes: {str(e)}")
        raise ValueError(f"Failed to convert image to bytes: {str(e)}")

def image_to_base64(image: ImageType) -> str:
    """
    Convert image to base64 string with data URI prefix.
    
    Args:
        image (ImageType): Image to convert (can be path, bytes, PIL Image, or file-like object)
        
    Returns:
        str: Base64 encoded image string with data URI prefix
        
    Raises:
        ValueError: If image format is invalid
    """
    try:
        # Если уже data URI
        if isinstance(image, str) and image.startswith('data:'):
            return image
            
        # Конвертируем в байты
        data = to_bytes(image)
        
        # Определяем MIME тип
        mime_type = is_accepted_format(data)
        
        # Кодируем в base64
        base64_data = base64.b64encode(data).decode('utf-8')
        
        return f"data:{mime_type};base64,{base64_data}"
        
    except Exception as e:
        logger.error(f"Failed to convert image to base64: {str(e)}")
        raise ValueError(f"Failed to convert image to base64: {str(e)}")

def extract_data_uri(data_uri: str) -> bytes:
    """
    Extracts the binary data from the given data URI.
    
    Args:
        data_uri (str): The data URI
        
    Returns:
        bytes: The extracted binary data
    """
    data = data_uri.split(",")[-1]
    return base64.b64decode(data)

