# How to get a cookie for BlackboxAPI

To use BlackboxAPI, you need a valid cookie from the blackbox.ai website. Here is a step-by-step guide to obtaining the necessary cookie:

1. Open a web browser and navigate to the [blackbox.ai](https://www.blackbox.ai) website.

2. Log in to your account if you haven't already.

3. Open the developer tools in your browser:
   - For Chrome/Edge: press F12 or right-click -> "View code"
   - For Firefox: press F12 or menu -> Web Development -> Web Developer Tools
   - For Safari: enable the "Develop" menu in settings, then select "Show Web Inspector"

4. Go to the "Network" tab in the developer tools.

5. Clear the current records in the Network panel by clicking the clear icon or pressing Ctrl+L (Cmd+K on Mac).

6. Send any message in the chat on the blackbox.ai website.

7. In the Network panel, find the request with the name "chat".

8. Select this request and go to the "Headers" tab.

9. Scroll down to the "Request Headers" section.

10. Find the line starting with "cookie:".

11. Copy the cookie value that starts with "sessionId=..." and ends before the next header.

Example cookie may look like this:

```
sessionId=abc123...xyz789
```

12. Save this cookie value - it will be needed to configure BlackboxAPI.

**Important:** Never share your cookie with others, as it provides access to your account.

## Using the cookie in BlackboxAPI

After obtaining the cookie, you need to write it when you first run BlackboxAPI `AIClient`:

```python
client = AIClient()
# When you run it, you will be prompted to enter the cookie, it will be saved in cookies.json file
# IMPORTANT: You should paste cookie WITH 'sessionId=' prefix
# like this:
# Enter cookie: sessionId=abc123...xyz789
```

BlackboxAPI will automatically load the cookie from this file when you initialize `AIClient`.

Remember that cookies may have a limited expiration time. If you encounter authentication errors, try to obtain a new cookie following these instructions.

