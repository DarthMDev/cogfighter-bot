import discord
from discord.ext import commands
import random
import json
client = commands.Bot(command_prefix = '.')
with open('config/config.json') as file:
	conf = json.load(file)

TOKEN = conf.get('token')

cogFighter = commands.Bot(command_prefix=conf.get('prefix'))
cogFighter.remove_command('help')
@client.event
async def on_ready():
    print('Cog Fighter Online.')

@commands.command()
@commands.cooldown(1, 300)
async def guessNumber(self, ctx):
    #TODO points system
    number = random.randint(1,100)
    tries = 5
    
    await ctx.send('guess the number between 1 and 100')
    message = await cogFighter.wait_for('message')
    guess = int(message.content)
    tries -= 1
    if tries <= 0:
        await ctx.send('You have ran out of tries. Try again later for another round.')
        return
    if guess > number:
        await ctx.send('Wrong, answer is bigger than that.')
    elif guess < number:
        await ctx.send('Wrong , answer is smaller than that')
    else:
        await ctx.send("Correct! You've won an award!")
        return

client.run(TOKEN)
