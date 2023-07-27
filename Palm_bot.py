import discord
import google.generativeai as palm
import nest_asyncio

# Configure the palm API with your API key
palm.configure(api_key="AIzaSyBT-uhDRqALsUofzl4miQphYxmggJZb6Jo")

# Default parameters for text generation
defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2},
    ],
}

nest_asyncio.apply()  # Patch asyncio to allow running the bot in a Jupyter Notebook

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def generate_response(message):
    if message.author == client.user:  # To avoid the bot responding to its own messages
        return

    # Get the content of the user's message as the prompt for text generation
    prompt = message.content

    # Generate the response using the palm API
    response = palm.generate_text(**defaults, prompt=prompt)

    # Send the generated response back to the same channel
    await message.channel.send(response.result)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    await generate_response(message)

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token
client.run('MTEzMzI4ODAyMDIwMDY2MTAwMg.Guh-XU.KA9MBq8cbq1dSDQQgiTNWXvySd5c5pUyRMCd6U')
