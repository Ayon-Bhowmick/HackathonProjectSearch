import os
import discord
from dotenv import load_dotenv
import VectorDB
from json import loads

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
    if message.content != "" and message.author != client.user:
        await message.channel.send("Searching...")
        query: str = message.content.replace("@HackathonSearchBot", "").strip()
        res = VectorDB.query(query, 10)
        projects = res["documents"][0]
        for proj in projects:
            await message.channel.send(proj)
        # projects = ", ".join([proj["project"] for proj in res["metadatas"][0]])
        # await message.channel.send(projects)

client.run(TOKEN)
