import discord
from discord.ext import commands, tasks
import json
from discord.ext.tasks import loop
import sqlite3
from threading import Thread
import os
from events import event
import time
import random
from collections import Counter
import bisect
import sqliteFuncs as db
with open('config/config.json') as file:
    conf = json.load(file)

TOKEN = conf.get('token')
PREFIX = conf.get('prefix')

cogFighter = commands.Bot(command_prefix=PREFIX)

# Gag constants
GAG_EMOS = ['<:cupcake:914821822875316224>', '<:fruitpieslice:914821822812409898>', '<:creampieslice:914821822598512702>', '<:fruitpie:914821822875320330>', '<:creampie:914821822229405726>', '<:bday:914821822715936788>', '<:wedding:914821822632067152>']
GAGS = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']
PRICES = [10, 20, 30, 40, 50, 60, 70]
THROW_DAMAGES = [5, 15, 25 , 50, 75, 115, 165, 225, 295, 375]
# Cog constants


def embedMsg(ctx, msg, title=''):
    emb = discord.Embed(title = title, description= msg)
    emb.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    return emb


def cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result


def choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]


@cogFighter.event
async def on_ready():
    print('Cog Fighter Online.')
    # t = Thread(target= event.Event(cogFighter).guessNumber)
    # t.start()


# This command will start the guess number event
@cogFighter.command()
@commands.has_any_role('Staff', 'staff', '🌌 Staff')
async def startGuessNumber(ctx):
    event.Event(cogFighter).guessNumber.start()


@cogFighter.command(aliases=['givemecrates', 'gibc', 'givecrates'])
async def giveMeCrates(ctx, num=100):
    await createAccount(ctx)
    db.add_crates(ctx.author.id, int(num))
    await ctx.send(embed=embedMsg(ctx, msg = f"There's {num} crates..."))


@cogFighter.command(aliases=['gibj','givemejb','givejb'])
async def giveMeJB(ctx, num=1000):
    db.add_balance(ctx.author.id, int(num))
    await ctx.send(embed=embedMsg(ctx, msg=f"{num} jellybeans have been added!", title=''))


@cogFighter.command(aliases=['setbal','setbalance','set'])
async def setjbBalance(ctx, num):
    db.set_value(ctx.author.id, 'balance', int(num))
    await ctx.send(embed=embedMsg(ctx, msg=f"balance has been set to {num}", title=''))


@cogFighter.command(aliases=['opencrates', 'oc'])
async def opencrate(ctx, arg=1):
    await createAccount(ctx)
    if arg < 0:
        await ctx.send(embed=embedMsg(ctx, "Cannot open a negative amount of crates."))
        return
    elif arg > 1000000:
        #Prevent overloading the bot
        await ctx.send(embed=embedMsg(ctx, 'You are opening too many crates at once. Please try again with a smaller number.'))
        return
    inv = db.fetch_data(ctx.author.id, 'inventory')

    if db.fetch_data(ctx.author.id, crates) >= arg:
        results = []
        counts = []
        for i in range(0, arg):
            
            result = choice(GAGS, [0.20, 0.19, 0.18, 0.16, 0.14, 0.09, 0.04])
            results.append(result)

        for i in range(len(GAGS)):

            counts.append(results.count(GAGS[i]))

        # display gags the user just recieved
        if arg == 1:
            title = f"You opened {str(arg)} crate and recieved:"
        else:
             title = f"You opened {str(arg)} crates and recieved:"
        message = ""
        for i in range(len(GAGS)):
            if counts[i] > 0:
                message += f"{GAG_EMOS[i]} {GAGS[i]} - {counts[i]}\n"

        inv = [counts[i] + int(inv[i]) for i in range(len(counts))]

        await ctx.send(embed=embedMsg(ctx, message, title))

        db.sub_crates(ctx.author.id, arg)
        db.set_value(ctx.author.id, 'inventory', inv)

    else:
        await ctx.send(embed=embedMsg(ctx, msg=f'You only have {str(db.fetch_data(ctx.author.id, "crates"))} crates.', title=''))


@cogFighter.command()
async def deleteinventory(ctx):
    await createAccount(ctx)
    db.set_value(ctx.author.id, 'inventory', [0, 0, 0, 0, 0, 0, 0])
    await ctx.send(embed=embedMsg(ctx, msg='Inventory deleted.', title=''))


async def createAccount(ctx):
    if not db.does_user_exist(ctx.author.id):
        db.create_user(ctx.author.id)
        await ctx.send(embed=embedMsg(ctx, msg="Account Created!", title=''))


@cogFighter.command(aliases=['inv', 'gags'])
async def inventory(ctx):
    await createAccount(ctx)

    inv = (db.fetch_data(ctx.author.id, 'inventory'))
    title = f"{ctx.author.name}#{ctx.author.discriminator}'s Inventory:"
    message = ''
    for i in range(len(GAGS)):
        # If the user has an amount of 0 for a  gag in the list of gags it will not show.
        if inv[i] > 0: message += f"{GAG_EMOS[i]} {GAGS[i]} x{inv[i]}\n"

    await ctx.send(embed=embedMsg(ctx, msg=message, title=title))


@cogFighter.command()
async def setupaccount(ctx):
    if db.does_user_exist(ctx.author.id):
        await ctx.send(embed=embedMsg(ctx, msg='You already have an account.'))
        return
    db.create_user(ctx.author.id)
    await ctx.send(embed=embedMsg(ctx, msg='Account created!', title=''))


#When finalizing this command, add a double check to ensure the user means to delete their account.
@cogFighter.command()
async def deleteaccount(ctx):
    if not db.does_user_exist(ctx.author.id):
        await ctx.send(embed=embedMsg(ctx, msg="No account found"))
        return
    db.remove_user(ctx.author.id)
    await ctx.send(embed=embedMsg(ctx, msg='Your account is now deleted.', title=''))

"""
@cogFighter.command()
async def givecrates(ctx, member: discord.Member = None, arg2=1):
    if member == None:
        member = ctx.author
    if 'crates ' + member.name not in db:
        db['crates ' + member.name] = 0
    db['crates ' + member.name] += arg2
    await ctx.send(member.name + ' has been given ' + str(arg2) + ' crates.')
"""

@cogFighter.command(aliases=['balance', 'bank', 'jar', 'bal'])
async def getbalance(ctx):
    await createAccount(ctx)
    await ctx.send(embed=embedMsg(ctx, msg=f'You have: {db.fetch_data(ctx.author.id, "balance")}' + ' jellybeans', title=''))


@cogFighter.command()
# @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def daily(ctx):
    await createAccount(ctx)
    hourWait = 24
    timeNow = time.time()
    if db.does_user_exist(ctx.author.id):
        data = db.fetch_data(ctx.author.id, 'dailycooldown')
        timeSinceLastClaimed = timeNow - data
        if (timeSinceLastClaimed / 3600) >= hourWait:
            db.add_crates(ctx.author.id, 1)
            db.set_value(ctx.author.id, 'dailycooldown', time.time())
            await ctx.send(embed=embedMsg(ctx, msg="Daily reward claimed!", title=''))
        else:
            await ctx.send(embed=embedMsg(ctx, msg=f'You have to wait {round(hourWait - (timeSinceLastClaimed / 3600))} hours. ', title=''))

    else:
        return


async def giveWeekly(ctx):
    db.add_crates(ctx.author.id, 3)
    db.add_balance(ctx.author.id, 5)
    await ctx.send(embed=embedMsg(ctx, msg="Weekly reward claimed!", title=''))

    db.set_value(ctx.author.id, 'weeklycooldown', time.time())


@cogFighter.command()
# @commands.cooldown(1, 604800, commands.BucketType.user)
async def weekly(ctx):
    await createAccount(ctx)
    if db.does_user_exist(ctx.author.id):
        data = db.fetch_data(ctx.author.id, 'weeklycooldown')
        timeSinceLastClaimed = time.time() - data
        if (timeSinceLastClaimed / (60 * 60 * 24)) >= 7:
            await giveWeekly(ctx)
        else:
            await ctx.send(embed=embedMsg(ctx, msg=f'You have to wait {round(7 - (timeSinceLastClaimed / (60 * 60 * 24)))} days. ', title=''))

    else:
        await giveWeekly(ctx)


@cogFighter.command(aliases=['c', 'crate'])
async def crates(ctx):
    await createAccount(ctx)
    value = db.fetch_data(ctx.author.id, 'crates')
    await ctx.send(embed=embedMsg(ctx, msg=f'You have: {value}' + ' crates', title=''))


@cogFighter.command()
async def racegame(ctx):
    await createAccount(ctx)

    bot1total = 0
    bot2total = 0
    bot3total = 0
    bot4total = 0
    usertotal = 0
    numberToWin = 20
    prize = 5

    def pred():
        return True


    while True:
        bot1num = random.randint(1, 4)
        bot2num = random.randint(1, 4)
        bot3num = random.randint(1, 4)
        bot4num = random.randint(1, 4)
        await ctx.send('Please select a number 1-4')
        message = await cogFighter.wait_for('message', timeout=300)
        try:
            numchosen = int(message.content)
            if numchosen > 4 or numchosen < 1:
                await ctx.send('must be 1-4')
                continue

        except:
            await ctx.send('must be an integer')
            continue

        await ctx.send(
            f'racer 1 chose {bot1num}, racer 2 chose {bot2num}, racer 3 chose {bot3num} and racer 4 chose {bot4num}')
        if bot1num != bot2num and bot1num != bot3num and bot1num != bot4num and bot1num != numchosen:
            bot1total += bot1num

        if bot2num != bot1num and bot2num != bot3num and bot2num != bot4num and bot2num != numchosen:
            bot2total += bot2num

        if bot3num != bot2num and bot3num != bot1num and bot3num != bot4num and bot3num != numchosen:
            bot3total += bot3num

        if bot4num != bot2num and bot4num != bot3num and bot4num != bot1num and bot4num != numchosen:
            bot4total += bot4num

        if numchosen != bot2num and numchosen != bot1num and numchosen != bot4num and numchosen != bot3num:
            usertotal += numchosen
        await ctx.send(
            f'Racer 1 has {bot1total} total, racer 2 has {bot2total} total, racer 3 has {bot3total} total, racer 4 has {bot4total} total and you have {usertotal} total.')
        if bot1total >= numberToWin:
            await ctx.send('Better luck next time bot 1 has won.')
            break
        if bot2total >= numberToWin:
            await ctx.send('Better luck next time bot 2 has won.')
            break
        if bot3total >= numberToWin:
            await ctx.send('Better luck next time bot 3 has won.')
            break
        if bot4total >= numberToWin:
            await ctx.send('Better luck next time bot 4 has won.')
            break
        if usertotal >= numberToWin:
            await ctx.send('You won ! Congrats!')
            await ctx.send(f'You won {prize} jellybeans.')
            db.add_balance(ctx.author.id, prize)
            break


@cogFighter.command()
# @commands.cooldown(1, 60, commands.BucketType.user)
async def flipcoin(ctx, arg=None, arg2=1):
    await createAccount(ctx)
    if not arg:
        await ctx.send(embed=embedMsg(ctx, msg="No arguments provided", title='Flipcoin'))
    if arg.lower() == 'heads' or arg.lower() == 'tails':
        if db.bal(ctx.author.id) >= int(arg2):
            db.sub_balance(ctx.author.id, arg2)
        else:
            await ctx.send(embed=embedMsg(ctx, msg='You do not have enough jellybeans.', title='Flipcoin'))
            return
    else:
        await ctx.send(embed=embedMsg(ctx, msg='Must supply tails or heads', title='Flipcoin'))
        flipcoin.reset_cooldown(ctx)
        return

    rand = random.randint(1, 2)
    if rand == 1:
        result = 'heads'
    elif rand == 2:
        result = 'tails'
    if arg.lower() == result:
        await ctx.send(embed=embedMsg(ctx, msg=f"Congrats! It landed on {result}, you earned {int(arg2) * 2} jellybeans!", title='Flipcoin'))
        db.add_balance(ctx.author.id, int(arg2)*2)
    else:
        await ctx.send(embed=embedMsg(ctx, msg=f'RIP. It landed on {result}', title='Flipcoin'))


# @cogFighter.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.CommandOnCooldown):
# 		em = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}", description=f"Try again in {round(error.retry_after)}" + "s.")
# 		await ctx.send(embed=em)



cogs = [
    "cogs.shop"
    # "cogs.events",
    # "cogs.commands",
    # "cogs.modcommands",
]
for cog in cogs:
    print(f'loading cog: {cog}')
    cogFighter.load_extension(cog)

if __name__ == "__main__":
    cogFighter.run(TOKEN)
