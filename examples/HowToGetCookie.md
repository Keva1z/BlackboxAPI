# 🍪 Getting Started with BlackboxAPI Authentication

A comprehensive guide to obtaining and configuring your authentication cookie for BlackboxAPI.

## 🔑 Prerequisites

- A web browser (Chrome, Firefox, Safari, or Edge)
- A registered account on [Blackbox AI](https://www.blackbox.ai)

## 🚀 Step-by-Step Guide

### 1️⃣ Access the Platform

1. Navigate to [blackbox.ai](https://www.blackbox.ai)
2. Log in to your account

### 2️⃣ Open Developer Tools

Choose your browser:

- **Chrome/Edge**: `F12` or Right-click → "View code"
- **Firefox**: `F12` or Menu → Web Development → Web Developer Tools
- **Safari**: Enable "Develop" menu in settings → Show Web Inspector

### 3️⃣ Capture the Cookie

1. Select the "Network" tab in Developer Tools
2. Clear existing records (`Ctrl+L` or `Cmd+K` on Mac)
3. Send any message in the Blackbox AI chat
4. Find the request named "chat"
5. Go to "Headers" tab
6. Locate "Request Headers"
7. Find the line starting with "cookie:"
8. Copy the value starting with `sessionId=`

Example format:
```bash
sessionId=abc123...xyz789
```

```python
client = AIClient()
# You'll be prompted for the cookie on first run
# Enter the complete cookie string:
# sessionId=abc123...xyz789
```

The cookie will be automatically saved to `cookies.json` for future use.

## 🔒 Security Notes

- **Never share** your cookie - it provides full account access
- Store `cookies.json` securely
- Exclude `cookies.json` from version control
- Cookies expire periodically - be prepared to refresh

## 🔄 Cookie Refresh

If you encounter authentication errors:

1. Delete existing `cookies.json`
2. Follow the cookie capture steps again
3. Restart your application

## 📝 Best Practices

- Implement proper error handling for authentication failures
- Consider implementing automatic cookie refresh
- Keep your login session active while using the API
- Monitor cookie expiration

## 🚨 Troubleshooting

Common issues and solutions:

- **Invalid Cookie Format**: Ensure you include the `sessionId=` prefix
- **Authentication Errors**: Your cookie might have expired
- **Missing Cookie File**: Follow the capture steps again
- **Access Denied**: Verify your account permissions

---

<p align="center">Need help? Just <a href="https://github.com/Keva1z/BlackboxAPI/issues">ask a question</a>!</p>