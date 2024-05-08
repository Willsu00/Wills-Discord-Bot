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





@bot.command(name='cmd')
async def cmd(ctx):
    embed_help = discord.Embed(
        title='Commands',
        description='**List of available commands:**\n\nPlay a game of slots:   `!spin`\nFlip a coin:   `!flip`',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_help)





@bot.command(name='spin')
async def spin(ctx):
    wheel1 = ['🍎', '🍌', '🍒', '🍓', '🍈']
    wheel2 = ['🍎', '🍌', '🍒', '🍓', '🍈']
    wheel3 = ['🍎', '🍌', '🍒', '🍓', '🍈']

    spin1 = random.choice(wheel1)
    spin2 = random.choice(wheel2)
    spin3 = random.choice(wheel3)

    if spin1 == spin2 == spin3:
        embed_slots = discord.Embed(
            title = 'Slots',
            description = f'{ctx.author.mention}\n\n**You Spun:**\n\n| {spin1} | {spin2} | {spin3} |\n\n🏆 **You Win!** 🏆',
            colour=discord.Colour.green()
        )
    else:
        embed_slots = discord.Embed(
            title = 'Slots',
            description = f'{ctx.author.mention}\n\n**You Spun:**\n\n| {spin1} | {spin2} | {spin3} |\n\n❌ **You Lose!** ❌',
            colour=discord.Colour.red()
        )

    await ctx.send(embed=embed_slots)
    



@bot.command(name='flip')
async def flip(ctx):
    coin = ['Heads','Tails']
    flip = random.choice(coin)

    if flip == 'Heads':
        embed_coin = discord.Embed(
            title = 'Coin Flip',
            description = f'{ctx.author.mention}\n\nYou got: **{flip}**!',
            colour=discord.Colour.green()
        )

        embed_coin.set_image(url='https://cdn-icons-png.freepik.com/256/3364/3364839.png')
    else:
        embed_coin = discord.Embed(
            title = 'Coin Flip',
            description = f'{ctx.author.mention}\n\nYou got: **{flip}**!',
            colour=discord.Colour.green()
        )

        embed_coin.set_image(url='https://cdn-icons-png.freepik.com/512/5448/5448175.png')

    await ctx.send(embed=embed_coin)




bot.run(TOKEN)

#### INVITE LINK: https://discord.com/oauth2/authorize?client_id=1236974255841873972&permissions=8&scope=bot