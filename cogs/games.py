from discord.ext import commands
import discord
from datetime import datetime
import json
import random

with open('config/config.json') as file:
	conf = json.load(file)
class Games(commands.Cog):
    def __init__(self, bot):
	    self.bot = bot


    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def guessNumber(self, ctx):
        tries = 30
        number = random.randint(1,100)
        await ctx.send('guess the number between 1 and 100')
        #TODO points system
        while tries > 0:
            message = await self.bot.wait_for('message')
            
            guess = int(message.content)
            tries -= 1

            if guess < number:
                await ctx.send('Wrong, answer is bigger than that.')
            elif guess > number:
                await ctx.send('Wrong , answer is smaller than that')
            else:
                await ctx.send("Correct! You've won an award!")
                break
        if tries <= 0:
            await ctx.send('You have ran out of tries. Try again later for another round.')
            return


def setup(bot):
	bot.add_cog(Games(bot))