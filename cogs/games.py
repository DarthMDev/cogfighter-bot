from discord.ext import commands
import discord
from datetime import datetime
import json
import random
import time
with open('config/config.json') as file:
	conf = json.load(file)
class Games(commands.Cog):
    def __init__(self, bot):
	    self.bot = bot


    """def countDownUserCoolDown(self, author):
        author.cooldown = 10
        while author.cooldown > 0:
            time.sleep(1)
            author.cooldown -= 1"""

    #@commands.command()
    #@commands.cooldown(1, 300, commands.BucketType.guild)

def setup(bot):
	bot.add_cog(Games(bot))