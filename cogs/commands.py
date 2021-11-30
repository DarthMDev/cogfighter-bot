from discord.ext import commands
import discord

from bot import PREFIX 
class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot








def setup(bot):
    bot.add_cog(Commands(bot))