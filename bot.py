import discord
from discord.ext import commands, tasks
import json
from discord.ext.tasks import loop
from replit import db
from threading import Thread
import os
from events import event
import time
import random
from collections import Counter
import bisect

with open('config/config.json') as file:
    conf = json.load(file)

TOKEN = conf.get('token')

cogFighter = commands.Bot(command_prefix=conf.get('prefix'))


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


def openLootbox():
    crateOptions = [':cupcake~1: Cupcake', ':fruitpieslice: Fruit Pie Slice', ':creampieslice: Cream Pie Slice', ':fruitpie: Fruit Pie', ':creampie: Cream Pie', ':bday: Birthday Cake', ':wedding~1: Wedding Cake', 'Special Gags (1-7)', 'Special Gags (8-14)']
    weights = [0.18, 0.18, 0.18, 0.13, 0.13, 0.08, 0.08, 0.038, 0.002]
    result = choice(crateOptions, weights)
    return result


@cogFighter.event
async def on_ready():
    print('Cog Fighter Online.')
    # t = Thread(target= event.Event(cogFighter).guessNumber)
    # t.start()


# This function can be called under a command decorator to check if the person calling the command has the staff role.
"""
def is_staff():
    def checkIfStaff(ctx):
        x = []
        for i in ctx.author.roles:
            x.append(i.name)
        return 'Staff' in x

    return commands.check(checkIfStaff)
"""

# This command will start the guess number event
@cogFighter.command()
@commands.has_any_role('Staff', 'staff', '🌌 Staff')
async def startGuessNumber(ctx):
    event.Event(cogFighter).guessNumber.start()


@cogFighter.command()
async def opencrate(ctx, arg=1):
    if 'crates ' + ctx.author.name not in db:
        db['crates ' + ctx.author.name] = 0
    if 'inventory ' + ctx.author.name not in db:
        db['inventory ' + ctx.author.name] = " "
    newInventory = list(db['inventory ' + ctx.author.name].split(','))

    if db['crates ' + ctx.author.name] >= arg:
        for i in range(0, arg):
            result = openLootbox()
            await ctx.send('You won a ' + result)
            newInventory.append(result)
            db['crates ' + ctx.author.name] -= 1

        db['inventory ' + ctx.author.name] = (','.join(newInventory))
    else:
        await ctx.send('You do not have enough crates.')


@cogFighter.command()
async def deleteinventory(ctx):
    del db['inventory ' + ctx.author.name]
    await ctx.send('Database entry deleted.')


@cogFighter.command()
async def inventory(ctx):
    if 'inventory ' + ctx.author.name not in db:
        db['inventory ' + ctx.author.name] = " "

    displayList = db['inventory ' + ctx.author.name]
    displayList = displayList.split(',')
    if ' ' in displayList:
        displayList.remove(' ')
    newList = [[x, displayList.count(x)] for x in set(displayList)]
    await ctx.send('Inventory: ' + str(newList))


@cogFighter.command()
async def setupaccount(ctx):
    db[ctx.author.name] = 0
    await ctx.send('Account is now setup.')


@cogFighter.command()
async def givecrates(ctx, member: discord.Member = None, arg2=1):
    if member == None:
        member = ctx.author
    if 'crates ' + member.name not in db:
        db['crates ' + member.name] = 0
    db['crates ' + member.name] += arg2
    await ctx.send(member.name + ' has been given ' + str(arg2) + ' crates.')


@cogFighter.command(aliases=['balance', 'bank', 'jar', 'bal'])
async def getbalance(ctx):
    if ctx.author.name not in db:
        db[ctx.author.name] = 0
        await ctx.send('Account is now setup.')
    await ctx.send('You have: {0}'.format(db[ctx.author.name]) + ' jellybeans')


@cogFighter.command()
async def deleteaccount(ctx):
    del db[ctx.author.name]
    await ctx.send('Your account is now deleted.')


async def giveCrate(ctx):
    if 'crates ' + ctx.author.name not in db:
        db['crates ' + ctx.author.name] = 0
    db['crates ' + ctx.author.name] += 1
    await ctx.send('You have been given 1 crate.')
    db[ctx.author.name + ' dailyCD'] = time.time()


@cogFighter.command()
# @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def daily(ctx):
    hourWait = 24
    timeNow = time.time()
    if ctx.author.name + ' dailyCD' in db:
        data = db[ctx.author.name + ' dailyCD']
        timeSinceLastClaimed = timeNow - data
        if (timeSinceLastClaimed / 3600) >= hourWait:
            await giveCrate(ctx)
        else:
            await ctx.send('You have to wait {0} hours. '.format(round(hourWait - (timeSinceLastClaimed / 3600))))

    else:
        await giveCrate(ctx)


async def giveWeekly(ctx):
    if 'crates ' + ctx.author.name not in db:
        db['crates ' + ctx.author.name] = 0
    if ctx.author.name not in db:
        db[ctx.author.name] = 0
    db['crates ' + ctx.author.name] += 3
    db[ctx.author.name] += 5
    await ctx.send("You have been awarded 3 crates and 5 jellybeans.")

    db[ctx.author.name + ' weeklyCD'] = time.time()


@cogFighter.command()
# @commands.cooldown(1, 604800, commands.BucketType.user)
async def weekly(ctx):
    daysWait = 7
    timeNow = time.time()

    if ctx.author.name + ' weeklyCD' in db:
        data = db[ctx.author.name + ' weeklyCD']
        timeSinceLastClaimed = timeNow - data
        if (timeSinceLastClaimed / (60 * 60 * 24)) >= daysWait:
            await giveWeekly(ctx)
        else:
            await ctx.send('You have to wait {0} days. '.format(round(daysWait - (timeSinceLastClaimed / (60 * 60 * 24)))))

    else:
        await giveWeekly(ctx)


@cogFighter.command()
async def crates(ctx):
    if 'crates {0}'.format(ctx.author.name) not in db:
        db['crates {0}'.format(ctx.author.name)] = 0

    value = db['crates {0}'.format(ctx.author.name)]
    await ctx.send('You have: {0}'.format(value) + ' crates')


@cogFighter.command()
async def racegame(ctx):
    bot1total = 0
    bot2total = 0
    bot3total = 0
    bot4total = 0
    usertotal = 0
    numberToWin = 20
    prize = 5

    def pred():
        return True

    if ctx.author.name not in db:
        db[ctx.author.name] = 0
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

        await ctx.send('racer 1 chose {0}, racer 2 chose {1}, racer 3 chose {2} and racer 4 chose {3}'.format(bot1num, bot2num, bot3num, bot4num))
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
        await ctx.send('Racer 1 has {0} total, racer 2 has {1} total, racer 3 has {2} total, racer 4 has {3} total and you have {4} total.'.format(bot1total, bot2total, bot3total, bot4total, usertotal))
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
            await ctx.send('You won {0} jellybeans.'.format(prize))
            db[ctx.author.name] += prize
            break


@cogFighter.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def flipcoin(ctx, arg=None, arg2=None):
    if not arg:
        await ctx.send('Must supply tails or heads')
        flipcoin.reset_cooldown(ctx)
        return
    if arg != 'heads' and arg != 'tails':
        await ctx.send('Must supply tails or heads')
        flipcoin.reset_cooldown(ctx)
        return
    if not arg2:
        arg2 = 1
    if ctx.author.name not in db:
        db[ctx.author.name] = 0
    if db[ctx.author.name] < int(arg2):
        await ctx.send('You do not have enough jellybeans.')
        return
    else:
        db[ctx.author.name] -= int(arg2)

    randomnum = random.randint(1, 2)
    if randomnum == 1:
        result = 'heads'
    elif randomnum == 2:
        result = 'tails'
    if arg == result:
        await ctx.send(
            'Congrats! It landed on {0} You won {1} jellybeans'.format(
                result,
                int(arg2) * 2))
        db[ctx.author.name] += int(arg2) * 2
    else:
        await ctx.send('RIP. It landed on {0}'.format(result))


# @cogFighter.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.CommandOnCooldown):
# 		em = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}", description="Try again in {0}".format(round(error.retry_after)) + "s.")
# 		await ctx.send(embed=em)


# cogs = [
#	'events.event',
# ]

# for cog in cogs:
# print('loading cog: {0}'.format(cog))
# cogFighter.load_extension(cog)

# @cogFighter.event
# async def on_command_error(ctx, error):
#   if isinstance(error, commands.CommandOnCooldown):
#    em = discord.Embed(title="Cooldown",description="Try again in {0}".format(round(error.retry_after)) + "s.")
#   await ctx.send(embed=em)
cogFighter.run(TOKEN)
