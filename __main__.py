import discord
import discord.ext.commands as commands
import os
from dotenv import load_dotenv
import random
import json

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)

load_dotenv()

def get_level(experience):
    try:
        return int(experience ** (1/3))
    except ValueError:
        return 1
    
def get_remaining_experience(experience):
    try:
        return (get_level(experience) + 1) ** 3 - experience
    except ValueError:
        return 1

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Get, set, GG')
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if "gg" in message.content.lower() or "ㅈㅈ" in message.content:
        await message.channel.send(random.choice(["gg", "ㅈㅈ"]))
        
        cnt = 1 # message.content.lower().count("gg") + message.content.count("ㅈㅈ")
        # print(cnt)
        with open('level.json', 'r') as f:
            users = json.load(f)
        
        await update_data(users, message.author)
        exp = await add_experience(users, message.author, cnt)
        await level_up(users, message.author, message, exp)
        
        with open('level.json', 'w') as f:
            json.dump(users, f)
        
    else:
        return
    
    
async def update_data(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]["experience"] = 0
        
async def add_experience(users, user, exp):
    users[str(user.id)]["experience"] += exp
    return exp
    
async def level_up(users, user, message, exp):
    experience = users[str(user.id)]["experience"]
    lvl_start = get_level(experience - exp)
    lvl_end = get_level(experience)
    if lvl_start < lvl_end:
        gif = random.choice(["https://tenor.com/view/gg-wp-good-game-well-played-ez-gif-21928504", "https://tenor.com/view/gg-ez-gif-25333310", "https://tenor.com/view/mario-luigi-gg-brothers-gif-5408209", "https://tenor.com/view/gg-gif-20863608"])
        embed = discord.Embed(title="GG", description=f"{user.mention} has GGed up to level {lvl_end}! GG")
        embed.set_image(url=gif)
        await message.channel.send(embed=embed)
        
async def reset_data(users, user):
    users[str(user.id)]["experience"] = 0


@bot.event
async def on_member_join(member):
    with open('level.json', 'r') as f:
        users = json.load(f)
        
    await update_data(users, member)
    
    with open('level.json', 'w') as f:
        json.dump(users, f)


@bot.hybrid_command(name='level', description='Check your level!')
async def level(ctx):
    with open('level.json', 'r') as f:
        users = json.load(f)

    await update_data(users, ctx.author)
    
    await ctx.send(f"{ctx.author.mention} is level {get_level(users[str(ctx.author.id)]['experience'])}\nOnly {get_remaining_experience(users[str(ctx.author.id)]['experience'])} GGs away from level {get_level(users[str(ctx.author.id)]['experience']) + 1}")
    

    with open('level.json', 'w') as f:
        json.dump(users, f)
        

@bot.hybrid_command(name='resetgg', description='Reset your level back to 0, be careful!')
async def resetgg(ctx):
    
    with open('level.json', 'r') as f:
        users = json.load(f)

    await reset_data(users, ctx.author)
    await ctx.send(f"{ctx.author.mention} has reset their level to 0, GG")

    with open('level.json', 'w') as f:
        json.dump(users, f)


bot.run(os.getenv('TOKEN'))