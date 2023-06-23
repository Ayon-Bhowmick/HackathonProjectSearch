import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents(messages=True))

@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n',
            f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_message(message):
    # send message to channel
    if message.content != "":
        await message.channel.send("Hello World!")

client.run(TOKEN)
