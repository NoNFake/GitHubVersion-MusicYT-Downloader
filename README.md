# GitHubVersion-MusicYT-Downloader

**Project Name:** YouTube Downloader Telegram Bot

**Description:**

This Python project creates a Telegram bot that allows users to download audio from YouTube videos. Users simply send the YouTube video URL to the bot, and it extracts the audio, retrieves the video title and thumbnail, and sends both the audio file and a message containing the title and link (for reference) to the user and a designated Telegram channel (optional).

**Key Features:**

- **YouTube Audio Download:** Extracts audio from YouTube videos at 128kbps AAC quality.
- **User-Friendly Interactions:** Accepts YouTube links (`https://www.youtube.com` or `https://youtu.be`) and provides clear messages for successful downloads or invalid links.
- **Channel Sharing (Optional):** Sends downloaded audio and information to a specified Telegram channel alongside a notification message (disabled for user privacy).
- **Error Handling:** Catches exceptions and sends appropriate error messages to the user.

**Requirements:**

- Python 3
- Libraries:
    - `telebot`
    - `pytube`
    - `Pillow`
    - `requests`
- A Telegram bot with appropriate permissions (obtainable via BotFather)
- A Telegram channel token (optional, for channel sharing)

**How to Use:**

1. **Set Up:**
    
    - Install the required libraries (`pip install telebot pytube Pillow requests`).
    - Create a `token.json` file containing your Telegram bot token and channel token (if applicable) in the following format:

``` JSON
{
    "bot": {
        "token": "YOUR_BOT_TOKEN"
    },
    "channel": {
        "token": "YOUR_CHANNEL_TOKEN" (optional)
    }
}
```
- Replace `YOUR_BOT_TOKEN` and `YOUR_CHANNEL_TOKEN` with your actual tokens.


1. **Run the Bot:**
    
    - Open a terminal or command prompt, navigate to the project directory, and execute:
    
    
    
    ``` Bash
    python main.py
    ```
