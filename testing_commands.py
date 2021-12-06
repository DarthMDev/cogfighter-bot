from bot_globals import *


@cogFighter.command(aliases=['givemecrates', 'gibc', 'givecrates'])
async def giveMeCrates(ctx, num=100):
    await createAccount(ctx)
    db.add_crates(ctx.author.id, int(num))
    await ctx.send(embed=embedMsg(ctx, msg=f"There's {num} crates..."))

@cogFighter.command(aliases=['setbal','setbalance','set'])
async def setjbBalance(ctx, num):
    db.set_value(ctx.author.id, 'balance', int(num))
    await ctx.send(embed=embedMsg(ctx, msg=f"balance has been set to {num}", title=''))

