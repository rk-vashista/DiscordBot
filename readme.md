# Discord Bot

Welcome to the Discord Bot project! 🎉 This bot uses Python and the `discord.py` library to interact with users and Groq's AI for smart responses.

## Setup

1. **Clone the Repo:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**

   ```bash
   pip install discord.py groq
   ```

3. **Set Up Your Keys:**

   Create a `.env` file with your Discord bot token and Groq API key:

   ```env
   BOT_KEY=your_discord_bot_token
   GROQ_KEY=your_groq_api_key
   ```

## How to Use

1. **Start the Bot:**

   ```bash
   python bot.py
   ```

2. **Chat with Your Bot:**

   - **Say `$hello`**: The bot will reply, "Oh Hie there!"
   - **Ask `$who are you?`**: The bot will say, "I am Elliot, a Discord Bot."
   - **Send Any Other Message**: The bot will use Groq to reply intelligently.

## Contribution

Have ideas or improvements? Feel free to contribute!

