import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ';')

@client.event
async def on_ready():
    print('Cog Fighter Online.')

client.run('Nzc0ODE3MzQ4NDQ4MTU3NzA2.X6dS4w.DgD2ZBOqbzSLi8QKwppmm6_BBLA')