import discord
from discord.ext import commands, tasks
import random
import json
from discord.ext.tasks import loop

from events import event 
with open('config/config.json') as file:
	conf = json.load(file)

TOKEN = conf.get('token')

cogFighter = commands.Bot(command_prefix=conf.get('prefix'))
@cogFighter.event
async def on_ready():
    print('Cog Fighter Online.')
    event.Event(cogFighter).guessNumber.start()

#cogs = [
#	'events.event',
#]

#for cog in cogs:
   # print('loading cog: {0}'.format(cog))
    #cogFighter.load_extension(cog)

#@cogFighter.event
#async def on_command_error(ctx, error):
 #   if isinstance(error, commands.CommandOnCooldown):
        #    em = discord.Embed(title="Cooldown",description="Try again in {0}".format(round(error.retry_after)) + "s.")
         #   await ctx.send(embed=em)
cogFighter.run(TOKEN)
