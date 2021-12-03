from discord.ext import commands, tasks
import discord
from datetime import datetime
import json
import random
import time
from discord.ext.tasks import loop
import asyncio
import sqlite_funcs as db
from threading import Thread
with open('config/config.json') as file:
	conf = json.load(file)      

class Event():  
    def __init__(self, bot: discord.Client()):
      self.bot = bot



    async def countDownUserCooldown(self, channel, author):
        db.set_value(author.id, 'userCooldown', 5)
        await channel.send("On cooldown please wait 5 seconds.")
        while db.fetch_value(author.id, 'userCooldown') > 0:
          time.sleep(1)
          db.sub_cooldown(author.id, 1)
        await channel.send('Cooldown is over.')
        

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
        
        while tries > 0:
            message = await self.bot.wait_for('message', check=pred)
            if message.author.id == '774817348448157706':
              continue
            try:
              guess = int(message.content)
            except ValueError:
             await channel.send('Must be an integer.')
             continue





            author = message.author
            if db.fetch_value(author.id, 'userCooldown'):
              db.set_value(author.id, 'userCooldown', 0)
            if db.fetch_value(author.id, 'userCooldown') <= 0:
              if guess < number:
                await channel.send('Wrong, answer is larger than that.')
                t2 = Thread(target = self.countDownUserCooldown(message.author))
                t2.start()
                await self.countDownUserCooldown(channel, message.author.name)
              elif guess > number:
                await channel.send('Wrong , answer smaller than that')
                t2 = Thread(target = self.countDownUserCooldown(message.author))
                t2.start()
                await self.countDownUserCooldown(channel, message.author)

              elif guess == number:

                await channel.send("Correct! {0} You've won an award!".format(message.author.mention))
                if db.does_user_exist():
                  db.set_value(author.id, 'userCooldown', 0)
                db.set_value(author.id, 'userCooldown', 5)
                await asyncio.sleep(600)
                break         
            else:
                await channel.send('You are on cooldown please wait {0} seconds'.format(str(db.fetch_value(author.id, 'userCooldown')) ))
        if tries <= 0:
                await channel.send('You have ran out of tries. Try again later for another round.')
                await asyncio.sleep(600)
                return
        
