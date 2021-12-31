import bisect
import random
from bot_globals import *


# Commands directly related to their user on the db
@cogFighter.command(aliases=['inv', 'gags'])
async def inventory(ctx):
    await createAccount(ctx)

    inv = (db.fetch_data(ctx.author.id, 'inventory'))
    title = f"{ctx.author.name}#{ctx.author.discriminator}'s Inventory:"
    message = ''
    for i in range(len(GAGS)):
        # If the user has an amount of 0 for a  gag in the list of gags it will not show.
        if inv[i] > 0:
            message += f"{GAG_EMOS[i]} {GAGS[i]} x{inv[i]}\n"

    await ctx.send(embed=embedMsg(ctx, msg=message, title=title))


@cogFighter.command()
async def deleteinventory(ctx):
    await createAccount(ctx)
    db.set_value(ctx.author.id, 'inventory', [0, 0, 0, 0, 0, 0, 0])
    await ctx.send(embed=embedMsg(ctx, msg='Inventory deleted.', title=''))


@cogFighter.command()
async def createaccount(ctx):
    if db.does_user_exist(ctx.author.id):
        await ctx.send(embed=embedMsg(ctx, msg='You already have an account.'))
        return
    db.create_user(ctx.author.id)
    await ctx.send(embed=embedMsg(ctx, msg='Account created!', title=''))


@cogFighter.command()
async def deleteaccount(ctx):
    if not db.does_user_exist(ctx.author.id):
        await ctx.send(embed=embedMsg(ctx, msg="No account found", title="Account Deletion"))
        return
    message = await ctx.send(
        embed=embedMsg(ctx, "Are you sure you want to delete your account?\nReact with ✅ to delete "
                            "your account. React with ❌ to cancel. (You can create a new one)",
                       title="Account Deletion"))
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    @cogFighter.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        if payload.member == cogFighter.user:
            return
        if payload.emoji.name == "✅" and ctx.author == payload.member and message.id == payload.message_id:
            await message.delete()
            db.remove_user(ctx.author.id)
            await ctx.send(embed=embedMsg(ctx, '', title="Your account has been deleted."))
        elif payload.emoji.name == "❌" and ctx.author == payload.member and message.id == payload.message_id:
            await message.delete()
            await ctx.send(embed=embedMsg(ctx, '', title="Account deletion cancelled."))


@cogFighter.command(aliases=['balance', 'bank', 'jar', 'bal'])
async def getbalance(ctx):
    await createAccount(ctx)
    await ctx.send(embed=embedMsg(ctx, msg=f'You have: {db.fetch_data(ctx.author.id, "balance")}' + ' jellybeans',
                                  title=''))


@cogFighter.command(aliases=['c', 'crate'])
async def crates(ctx):
    await createAccount(ctx)
    value = db.fetch_data(ctx.author.id, 'crates')
    await ctx.send(embed=embedMsg(ctx, msg=f'You have: {value}' + ' crates', title=''))


# Functions for crate opening
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


@cogFighter.command(aliases=['opencrates', 'oc'])
async def opencrate(ctx, arg=1):
    await createAccount(ctx)
    if arg <= 0 or arg > 1000000:
        await ctx.send(embed=embedMsg(ctx, f"Cannot open {str(arg)} crates."))
        return

    inv = db.fetch_data(ctx.author.id, 'inventory')

    if db.fetch_data(ctx.author.id, 'crates') >= arg:
        results = []
        counts = []
        for i in range(0, arg):
            result = choice(GAGS, [0.20, 0.19, 0.18, 0.16, 0.14, 0.09, 0.04])
            results.append(result)

        for i in range(len(GAGS)):
            counts.append(results.count(GAGS[i]))

        # display gags the user just received
        # if argument is 1 use singular "crate" in the message 
        # else use plural "crates" in the message 
        title = f"You opened {str(arg)} crate{'' if arg == 1 else 's'} and received:"
        message = ""
        for i in range(len(GAGS)):
            if counts[i] > 0:
                message += f"{GAG_EMOS[i]} {GAGS[i]} - {counts[i]}\n"

        inv = [counts[i] + int(inv[i]) for i in range(len(counts))]

        await ctx.send(embed=embedMsg(ctx, message, title))

        db.sub_crates(ctx.author.id, arg)
        db.set_value(ctx.author.id, 'inventory', inv)

    else:
        if db.fetch_data(ctx.author.id, "crates") > 1:
            await ctx.send(embed=embedMsg(ctx, msg=f'You only have {str(db.fetch_data(ctx.author.id, "crates"))} crates.',
                                      title=''))
        elif db.fetch_data(ctx.author.id, "crates") == 1:
            await ctx.send(embed=embedMsg(ctx, msg='You only have 1 crate.'))
        else:
            await ctx.send(embed=embedMsg(ctx, msg='You do not have any crates.'))
