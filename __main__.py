import discord
import os
from dotenv import load_dotenv
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()

@client.event
async def on_ready():
    print('Get, set, GG')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "gg" in message.content.lower() or "ㅈㅈ" in message.content:
        await message.channel.send(random.choice(["gg", "ㅈㅈ"]))
    else:
        return


client.run(os.getenv('TOKEN'))