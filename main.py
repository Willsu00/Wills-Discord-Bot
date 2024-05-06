import discord
import os
import random
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.content.startswith('hello'):
        await message.channel.send('world!')
    await bot.process_commands(message)

@bot.command(name='ping')
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention} pong!')


@bot.command(name='spin')
async def spin(ctx):
    wheel1 = ['🍎', '🍌', '🍒', '🍓', '🍈']
    wheel2 = ['🍎', '🍌', '🍒', '🍓', '🍈']
    wheel3 = ['🍎', '🍌', '🍒', '🍓', '🍈']

    spin1 = random.choice(wheel1)
    spin2 = random.choice(wheel2)
    spin3 = random.choice(wheel3)

    await ctx.send(f'{ctx.author.mention}\n You Spun:\n | {spin1} | {spin2} | {spin3} | ')

    if spin1 == spin2 == spin3:
        await ctx.send('You win!')
    else:
        await ctx.send('You lost!')
    

bot.run(TOKEN)

