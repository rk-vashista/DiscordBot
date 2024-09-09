import discord
from discord.ext import commands
import os
from gradio_client import Client
import requests
from groq import Groq  # Ensure this module is installed

bot_id = os.getenv('BOT_KEY')
groq_key = os.getenv('GROQ_KEY')

# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Initialize the Groq client
groq_client = Groq(api_key=groq_key)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def send_image_embed(channel, image_path):
    """Sends an image as an embed in the specified channel."""
    with open(image_path, 'rb') as image_file:
        await channel.send(file=discord.File(image_file, 'generated_image.png'))

async def send_message(channel, message):
    """Sends a message to the specified channel."""
    await channel.send(message)

def generate_img(prompt):
    client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")
    result = client.predict(
        height=1024,
        width=1024,
        steps=8,
        scales=3.5,
        prompt=prompt,
        seed=3413,
        api_name="/process_image"
    )

    image_url = result  # Adjust this if the URL is nested within the result

    # Check if the URL is a local file path
    if os.path.isfile(image_url):
        with open(image_url, "rb") as file:
            content = file.read()
        with open("output_filename.png", "wb") as file:
            file.write(content)
    else:
        # Download the image from the web URL
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("output_filename.png", "wb") as file:
                file.write(response.content)
        else:
            print("Failed to download image")
            return
    return

@bot.command()
async def generate(ctx, *, prompt: str):
    generate_img(prompt)
    await send_image_embed(ctx.channel, 'output_filename.png')
    if os.path.exists('output_filename.png'):
        os.remove('output_filename.png')
    

async def handle_normal_conversation(message):
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": message.content}],
        model="llama3-groq-70b-8192-tool-use-preview"
    )
    response = chat_completion.choices[0].message.content
    await message.channel.send(response)

    if "<tool_call>" in response and "</tool_call>" in response:
        response = "Failed to generate"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        content = message.content.replace(f'<@!{bot.user.id}>', '').strip()
        if content.startswith('generate'):
            prompt = content[len('generate'):].strip()
            await generate(await bot.get_context(message), prompt=prompt)
        else:
            await handle_normal_conversation(message)
    else:
        await bot.process_commands(message)


print(groq_client)

# Run the bot with your token
bot.run(bot_id)


