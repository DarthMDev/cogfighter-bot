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

gagEmos = ['<:cupcake:914821822875316224> Cupcake', '<:fruitpieslice:914821822812409898> Fruit Pie Slice', '<:creampieslice:914821822598512702> Cream Pie Slice', '<:fruitpie:914821822875320330> Fruit Pie', '<:creampie:914821822229405726> Cream Pie', '<:bday:914821822715936788> Birthday Cake', '<:wedding:914821822632067152> Wedding Cake']
gags = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']


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
async def giveMeCrates(ctx, num):
    await createAccount(ctx)
    db.add_crates(ctx.author.id, int(num))
    await ctx.send(f"There's {num} crates...")


@cogFighter.command(aliases=['gibj','givemejb','givejb'])
async def giveMeJB(ctx, num):
    db.add_balance(ctx.author.id, int(num))
    await ctx.send(f"{num} jellybeans have been added!")


@cogFighter.command(aliases=['setbal','setbalance','set'])
async def setjbBalance(ctx, num):
    db.set_value(ctx.author.id, 'balance', int(num))
    await ctx.send(f"balance has been set to {num}")


@cogFighter.command(aliases=['opencrates', 'oc'])
async def opencrate(ctx, arg=1):
    await createAccount(ctx)

    inv = db.fetch_data(ctx.author.id, 'inventory')

    if db.fetch_data(ctx.author.id, crates) >= arg:
        results = []
        counts = []
        for i in range(0, arg):
            
            result = choice(gags, [0.18, 0.18, 0.18, 0.13, 0.13, 0.118, 0.082])
            results.append(result)

        for i in range(len(gags)):

            counts.append(results.count(gags[i]))

        # display gags the user just recieved
        message = f"You opened {str(arg)} crate(s) and recieved:"
        for i in range(len(gags)):
            if counts[i] > 0:
                message += f"\n{gagEmos[i]} x{counts[i]}"

        inv = [counts[i] + int(inv[i]) for i in range(len(counts))]

        await ctx.send(message)

        db.sub_crates(ctx.author.id, arg)
        db.set_value(ctx.author.id, 'inventory', inv)

    else:
        await ctx.send('You only have {} crates.'.format(str(db.fetch_data(ctx.author.id, 'crates'))))


@cogFighter.command()
async def deleteinventory(ctx):
    await createAccount(ctx)
    db.set_value(ctx.author.id, 'inventory', [0, 0, 0, 0, 0, 0, 0])
    await ctx.send('Inventory deleted.')


async def createAccount(ctx):
    if not db.does_user_exist(ctx.author.id):
        db.create_user(ctx.author.id)
        await ctx.send("Account Created!")


@cogFighter.command(aliases=['inv', 'gags'])
async def inventory(ctx):
    await createAccount(ctx)

    inv = (db.fetch_data(ctx.author.id, 'inventory'))
    message = f"{ctx.author.name}#{ctx.author.discriminator}'s Inventory:"
    for i in range(len(gags)):
        # If the user has an amount of 0 for a  gag in the list of gags it will not show.
        if inv[i] > 0: message += f"\n{gagEmos[i]} x{inv[i]}"

    await ctx.send(message)


@cogFighter.command()
async def setupaccount(ctx):
    db.create_user(ctx.author.id)
    await ctx.send('Account created!')


#When finalizing this command, add a double check to ensure the user means to delete their account.
@cogFighter.command()
async def deleteaccount(ctx):
    db.remove_user(ctx.author.id)
    await ctx.send('Your account is now deleted.')

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
    await ctx.send('You have: {0}'.format(db.fetch_data(ctx.author.id, 'balance')) + ' jellybeans')


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
            await ctx.send("Daily reawrd claimed!")
        else:
            await ctx.send('You have to wait {0} hours. '.format(round(hourWait - (timeSinceLastClaimed / 3600))))

    else:
        return


async def giveWeekly(ctx):
    db.add_crates(ctx.author.id, 3)
    db.add_balance(ctx.author.id, 5)
    await ctx.send("Weekly reward claimed!")

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
            await ctx.send('You have to wait {0} days. '.format(round(7 - (timeSinceLastClaimed / (60 * 60 * 24)))))

    else:
        await giveWeekly(ctx)


@cogFighter.command()
async def crates(ctx):
    await createAccount(ctx)
    value = db.fetch_data(ctx.author.id, 'crates')
    await ctx.send('You have: {0}'.format(value) + ' crates')


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
            db.add_balance(ctx.author.id, prize)
            break


@cogFighter.command()
# @commands.cooldown(1, 60, commands.BucketType.user)
async def flipcoin(ctx, arg=None, arg2=1):
    await createAccount(ctx)
    if not arg:
        await ctx.send("No arguments provided")
    if arg.lower() == 'heads' or arg.lower() == 'tails':
        if db.bal(ctx.author.id) >= int(arg2):
            db.sub_balance(ctx.author.id, arg2)
        else:
            await ctx.send('You do not have enough jellybeans.')
            return
    else:
        await ctx.send('Must supply tails or heads')
        flipcoin.reset_cooldown(ctx)
        return

    rand = random.randint(1, 2)
    if rand == 1:
        result = 'heads'
    elif rand == 2:
        result = 'tails'
    if arg.lower() == result:
        await ctx.send(f"Congrats! It landed on {result}, you earned {int(arg2) * 2} jellybeans!")
        db.add_balance(ctx.author.id, int(arg2)*2)
    else:
        await ctx.send('RIP. It landed on {0}'.format(result))


# @cogFighter.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.CommandOnCooldown):
# 		em = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}", description="Try again in {0}".format(round(error.retry_after)) + "s.")
# 		await ctx.send(embed=em)



cogs = [
    "cogs.shop"
    # "cogs.events",
    # "cogs.commands",
    # "cogs.modcommands",
]
for cog in cogs:
    print('loading cog: {0}'.format(cog))
    cogFighter.load_extension(cog)

if __name__ == "__main__":
    cogFighter.run(TOKEN)
