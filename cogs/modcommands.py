from discord.ext import commands
from bot_globals import *
# import sqliteFuncs as db

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logchannel = cogFighter.get_channel(926888860837888100)

    # @commands.command()
    # @commands.has_role('Discord Moderation Team')
    # async def mute(self, context, name: discord.Member):
    #     roleMuted = discord.utils.get(context.guild.roles, name='Muted')
    #     await name.add_roles(roleMuted)
    #     embedMessage = discord.Embed(title='User is now muted!',
    #                                  description=f'**{name}** was muted by **{context.message.author}**!')
    #     await self.logchannel.send(embed=embedMessage)
    #
    # @commands.command()
    # @commands.has_role('Discord Moderation Team')
    # async def unmute(self, context, name: discord.Member):
    #     roleMuted = discord.utils.get(context.guild.roles, name='Muted')
    #     await name.remove_roles(roleMuted)
    #     embedMessage = discord.Embed(title='User is now unmuted!',
    #                                  description=f'**{name}** was unmuted by **{context.message.author}**!')
    #     await self.logchannel.send(embed=embedMessage)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member=None, duration="7"):
        if member == None:
            await ctx.author.send("Please specify a user to be banned.")
            await ctx.message.delete()
            return
        member = await discord.ext.commands.MemberConverter().convert(ctx, member)
        try:
            await ctx.guild.ban(member)
            await self.logchannel.send(embed=embedMsg(ctx, msg=f"**{member}** [{member.id}] was banned."))
        except:
            await ctx.author.send(f"{member.name} could not be banned.")
        await ctx.message.delete()


    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, context, name: discord.Member, *, reason='No reason given.'):
        await context.guild.unban(name, reason=reason)
        embedMessage = discord.Embed(title='User is now unbanned!',
                                     description=f'**{name}** was unbanned by **{context.message.author}** for **{reason}**')
        await self.logchannel.send(embed=embedMessage)

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, context, name: discord.Member, *, reason='No reason given.'):
        await context.guild.kick(name, reason=reason)
        embedMessage = discord.Embed(title='User has been kicked!',
                                     description=f'**{name}** was kicked by **{context.message.author}** for **{reason}**')
        await self.logchannel.send(embed=embedMessage)

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def giverole(self, context, name: discord.Member, role: discord.Role):
        await name.add_roles(role)

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def removerole(self, context, name: discord.Member, role: discord.Role):
        await name.remove_roles(role)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def clean(self, context, number: int):
        await self.logchannel.channel.purge(limit=number + 1)

    # @commands.command()
    # @commands.has_any_role("Dev Team", "Discord Administration Team")
    # async def resetdb(self, context):
    #     db.clear_db()
    #     await context.send(' Database has been cleared.')

    # @commands.command()
    # @commands.has_any_role("Dev Team", "Discord Administration Team")

    # async def getdb(self, context):
    #     #TODO
    #     """
    #     Displays the entire database in a nice format.
    #     """
    #     pass


def setup(bot):
    bot.add_cog(ModCommands(bot))
