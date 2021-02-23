from discord.ext import commands, tasks
import discord
from datetime import datetime
import json
import random
import time
from discord.ext.tasks import loop
import asyncio
with open('config/config.json') as file:
	conf = json.load(file)
class Event(object):
    def __init__(self, bot: discord.Client()):
        self.bot = bot

    @loop(seconds=600)
    async def guessNumber(self):

        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(813541240003887142)
        def pred(m):
            return m.channel == channel
        #while not self.bot.is_closed:
        tries = 30
        number = random.randint(1,100)
        await channel.send('guess the number between 1 and 100')
        #TODO points system
        while tries > 0:
            message = await self.bot.wait_for('message', check=pred)
            
            try:
                guess = int(message.content)
            except: 
                await channel.send('must be an integer')
                continue
            tries -= 1
            #if author.cooldown:
                #   if message.author.cooldown >=0:
            if guess < number:
                await channel.send('Wrong, answer is bigger than that.')
                        #self.countDownUserCooldown(message.author)
            elif guess > number:
                await channel.send('Wrong , answer is smaller than that')
                #self.countDownUserCooldown(message.author)

            elif guess == number:

                await channel.send("Correct! {0} You've won an award!".format(message.author.mention))
                break
        await asyncio.sleep(600)
            #else:
                 #   channel.send('You are on cooldown please wait {0} seconds'.format(author.cooldown))
        if tries <= 0:
                await channel.send('You have ran out of tries. Try again later for another round.')
                await asyncio.sleep(600)
                return
        
