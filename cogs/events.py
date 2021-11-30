from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == 'suggestions':
            await message.add_reaction('✅')
            await message.add_reaction('❌')





def setup(bot):
    bot.add_cog(Events(bot))