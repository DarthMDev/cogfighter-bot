import sys
sys.path.append(".")
from events import event
import time
from inventory import *
from testing_commands import *


# This command will start the guess number event
@cogFighter.command()
@commands.has_any_role('Staff', 'staff', '🌌 Staff')
async def startGuessNumber(ctx):
    event.Event(cogFighter).guessNumber.start()


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
            await ctx.send(embed=embedMsg(ctx,
                                          msg=f'You have to wait {round(hourWait - (timeSinceLastClaimed / 3600))} hours. ',
                                          title=''))

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
            await ctx.send(embed=embedMsg(ctx,
                                          msg=f'You have to wait {round(7 - (timeSinceLastClaimed / (60 * 60 * 24)))} days. ',
                                          title=''))

    else:
        await giveWeekly(ctx)


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
        await ctx.send(embed=embedMsg(ctx,
                                      msg=f"Congrats! It landed on {result}, you earned {int(arg2) * 2} jellybeans!",
                                      title='Flipcoin'))
        db.add_balance(ctx.author.id, int(arg2) * 2)
    else:
        await ctx.send(embed=embedMsg(ctx, msg=f'RIP. It landed on {result}', title='Flipcoin'))


# @cogFighter.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.CommandOnCooldown):
# 		em = discord.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator}", description=f"Try again in {round(error.retry_after)}" + "s.")
# 		await ctx.send(embed=em)


cogs = [
    "cogs.shop",
    "cogs.suits",
    # "cogs.events",
    # "cogs.commands",
    "cogs.modcommands"
]
@cogFighter.event
async def on_ready():
    for cog in cogs:
        print(f'loading cog: {cog}')
        cogFighter.load_extension(cog)
    print('Cog Fighter Online.')

if __name__ == "__main__":
    cogFighter.run(TOKEN)
