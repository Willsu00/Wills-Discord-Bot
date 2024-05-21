import discord
import os
import random
import sqlite3
from discord.ext import commands
from discord.ext.commands import BucketType, CommandOnCooldown
from sqlite3 import Error
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot_version = 0.1

def create_connection():
    connection = None;
    try:
        connection = sqlite3.connect('currency.db')
    except Error as e:
        print(e)
    return connection

def create_table(connection):
    try:
        cursor = connection.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS currency (
                    user_id TEXT PRIMARY KEY,
                    balance INTEGER NOT NULL
                );'''
        cursor.execute(sql)
    except Error as e:
        print(e)

connection = create_connection()

if connection is not None:
    create_table(connection)

def check_balance(connection, user_id):
    sql = '''SELECT balance FROM currency WHERE user_id = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,(user_id,))
    return cursor.fetchone()

def add_balance(connection, user_id, balance):
    sql = '''INSERT INTO currency(user_id, balance) VALUES(?,?)'''
    cursor = connection.cursor()
    cursor.execute(sql, (user_id, balance))
    connection.commit()

def update_balance(connection, user_id, balance):
    sql = '''UPDATE currency SET balance = ? WHERE user_id = ?'''
    cursor = connection.cursor()
    cursor.execute(sql, (balance, user_id))
    connection.commit()

def get_create_balance(connection, user_id):
    balance = check_balance(connection, user_id)
    if balance is None:
        add_balance(connection, user_id, 0)
        balance = check_balance(connection, user_id)
        return 0
    else:
        return balance[0]


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'{bot.user.name} is online! {round(bot.latency * 1000)}ms')


@bot.command(name='commands')
async def commands(ctx):
    embed_help = discord.Embed(
        title='Commands',
        description='**List of available commands:**\n\nPlay a game of slots: `!spin`\nFlip a coin: `!flip`\nRoll a dice: `!roll`\nClaim hourly points: `!claim`\nCheck balance: `!balance` or `!balance of @user`\nTrade points: `!trade amount [amount] @user`',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_help)



@bot.group(invoke_without_command=True)
async def uid(ctx):
    user_id = str(ctx.author.id)
    connection = create_connection()
    get_create_balance(connection, user_id)
    check_balance(connection, user_id)
    await ctx.send(f"{ctx.author.mention}'s Pokies ID: {user_id}")

@uid.command(name='of')
async def uid_user(ctx, user: discord.Member):
    user_id = str(user.id)
    connection = create_connection()
    get_create_balance(connection, user_id)
    check_balance(connection, user_id)
    await ctx.send(f"{user}'s Pokies ID: {user_id}")



@bot.command(name='spin')
async def spin(ctx):
    user_id = str(ctx.author.id)
    connection = create_connection()
    get_create_balance(connection, user_id)
    check_balance(connection, user_id)
    if check_balance(connection, user_id)[0] < 10:
        embed_spinError = discord.Embed(
            title = 'Spin Error!',
            description = 'Sorry, you do not have enough points to spin. You need at least 10 points to play.',
            color=discord.Color.red()
        )
        embed_spinError.add_field(name='', value=f'{ctx.author.mention}',inline=True)
        await ctx.send(embed=embed_spinError)
        return
    else:
        new_balance = check_balance(connection, user_id)[0] - 10
        

        wheel1 = ['🍎', '🍒', '🍓', '🍈'] * 10 + ['🍌'] * 6 + ['🤑'] * 3
        wheel2 = ['🍎', '🍌', '🍒', '🍈'] * 4 + ['🍓'] * 4 + ['🤑'] * 3
        wheel3 = ['🍎', '🍌', '🍒', '🍓'] * 20 + ['🍈'] * 10 + ['🤑'] * 3

        spin1 = random.choice(wheel1)
        spin2 = random.choice(wheel2)
        spin3 = random.choice(wheel3)

        if spin1=='🤑' and spin2 == '🤑' and spin3 =='🤑':
            embed_slots = discord.Embed(
                title = 'Slots',
                description = f'{ctx.author.mention}\n\n**You Spun:**\n\n| {spin1} | {spin2} | {spin3} |\n\n💰💴💰 **MEGA JACKPOT!** 💰💴💰',
                colour=discord.Colour.yellow()
            )
            new_balance += 1000

        elif spin1 == spin2 == spin3:
            embed_slots = discord.Embed(
            title = 'Slots',
            description = f'{ctx.author.mention}\n\n**You Spun:**\n\n| {spin1} | {spin2} | {spin3} |\n\n💰 **JACKPOT!** 💰',
            colour=discord.Colour.yellow()
            )
            new_balance += 200
        elif spin2==spin3 or spin2==spin1:
            embed_slots = discord.Embed(
                title = 'Slots',
                description = f'{ctx.author.mention}\n\n**You Spun:**\n\n| {spin1} | {spin2} | {spin3} |\n\n🏆 **You Win!** 🏆',
                colour=discord.Colour.green()
            )
            new_balance += 30
        else:
            embed_slots = discord.Embed(
                title = 'Slots',
                description = f'{ctx.author.mention}\n\n**You Spun:**\n\n| {spin1} | {spin2} | {spin3} |\n\n❌ **You Lose!** ❌',
                colour=discord.Colour.red()
            )
        update_balance(connection, user_id, new_balance)
    
    await ctx.send(embed=embed_slots)


from discord.ext import commands

@bot.command(name='claim')
@commands.cooldown(1, 86400, BucketType.user)
async def claim(ctx):
    user_id = str(ctx.author.id)
    connection = create_connection()
    get_create_balance(connection, user_id)
    balance = check_balance(connection, user_id)
    if balance is None:
        balance = [0]
    new_balance = balance[0] + 200
    update_balance(connection, user_id, new_balance)
    embed_claim = discord.Embed(
        title='Claim',
        description=f"{ctx.author.mention} claimed 200 points! Your new balance is {new_balance}.",
        color=discord.Color.green()
    )

    await ctx.send(embed=embed_claim)

@claim.error
async def claim_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        embed_claimError = discord.Embed(
            title='Claim Error!',
            description='Sorry, you can only claim your points once every 24 hours. Please try again in **{:.0f} hours.**'.format(
                error.retry_after / 3600),
            color=discord.Color.red()
        )

        embed_claimError.add_field(name='', value=f'{ctx.author.mention}', inline=True)
    else:
        raise error
    await ctx.send(embed=embed_claimError)


# All in: gives users 10% chance for a double or nothing.

@bot.group(invoke_without_command=True)
async def trade(ctx):
    embed_trade = discord.Embed(
        title='Trade',
        description='Trade using `!trade [amount] @user` command'
    )
    await ctx.send(embed=embed_trade)

@trade.command(name='amount')
async def trade_user(ctx, amount: int, user: discord.Member):
    if amount <= 0:
        embed_tradeError = discord.Embed(
            title='Trade Error',
            description=f'{ctx.author.mention}, you cannot trade a negative or zero amount of points.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_tradeError)
        return

    sender_id = str(ctx.author.id)
    receiver_id = str(user.id)
    
    if sender_id == receiver_id:
        embed_tradeError = discord.Embed(
            title='Trade Error',
            description=f'{ctx.author.mention}, you cannot trade with yourself.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_tradeError)
        return
    
    connection = create_connection()
    sender_balance = check_balance(connection, sender_id)
    receiver_balance = check_balance(connection, receiver_id)
    if sender_balance is None or sender_balance[0] < amount:
        embed_tradeError = discord.Embed(
            title='Trade Error',
            description=f'{ctx.author.mention}, you do not have enough points to trade.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_tradeError)
        return
    else:
        update_balance(connection, sender_id, sender_balance[0] - amount)
        update_balance(connection, receiver_id, receiver_balance[0] + amount)

        embed_tradeSuccess = discord.Embed(
            title='Trade',
            description=f'{ctx.author.mention} traded {amount} points to {user.mention}.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed_tradeSuccess)



@bot.group(invoke_without_command=True)
async def balance(ctx):
    user_id = str(ctx.author.id)
    connection = create_connection()
    balance = check_balance(connection, user_id)
    if balance is None:
        balance = [0]
    embed_balance = discord.Embed(
        title='Balance',
        description=f'{ctx.author.mention}, your balance is {balance[0]}.',
        color=discord.Color.teal()
    )
    await ctx.send(embed=embed_balance)

@balance.command(name='of')
async def balance_user(ctx, user: discord.Member):
    user_id = str(user.id)
    connection = create_connection()
    balance = check_balance(connection, user_id)
    if balance is None:
        balance = [0]
    embed_balance = discord.Embed(
        title='Balance',
        description=f"{user}'s balance is {balance[0]}.",
        color=discord.Color.teal()
    )
    await ctx.send(embed=embed_balance)




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


@bot.command(name='roll')
async def roll(ctx):
    dice = ['1','2','3','4','5','6']
    roll = random.choice(dice)

    embed_dice = discord.Embed(
        title = 'Dice Roll',
        description = f'{ctx.author.mention}\n\nYou rolled:\n🎲 **{roll}**! 🎲',
        colour=discord.Colour.teal()
    )

    await ctx.send(embed=embed_dice)


bot.run(TOKEN)


