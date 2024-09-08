import discord
import os
from groq import Groq  # Ensure this module is installed and correctly imported

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

client = discord.Client(intents=intents)  # connection to the Discord
bot_id = os.getenv('BOT_KEY')
groq_key = os.getenv('GROQ_KEY')  # Corrected variable name for consistency

groq_client = Groq(
    api_key=groq_key,
)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

MAX_MESSAGE_LENGTH = 2000  # Max length for Discord messages

def split_message(message):
    """Split a message into chunks of MAX_MESSAGE_LENGTH characters."""
    return [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        if message.content.startswith('$hello'):
            await message.channel.send('Oh Hie there!')
        elif message.content.startswith('$who are you?'):
            await message.channel.send('I am Elliot, a Discord Bot')
        else:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message.content,
                    }
                ],
                model="llama3-groq-70b-8192-tool-use-preview",
            )
            response = chat_completion.choices[0].message.content

            if len(response) > MAX_MESSAGE_LENGTH:
                # Split the response into manageable chunks and send each
                for chunk in split_message(response):
                    await message.channel.send(chunk)
            else:
                # Send the message directly if it's within the length limit
                await message.channel.send(response)

client.run(bot_id)