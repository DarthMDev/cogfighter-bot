from discord.ext import commands
from bot_globals import *
from datetime import timedelta


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logchannel = cogFighter.get_channel(MOD_LOG_CHANNEL)

    @commands.command(aliases=['timeout'])
    @commands.has_role('Discord Moderation Team')
    async def mute(self, ctx, member=None, duration=1):
        if member is None:
            await ctx.author.send("Please specify a user to be muted.")
            await ctx.message.delete()
            return

        try:
            member = await discord.ext.commands.MemberConverter().convert(ctx, member)
            await member.timeout_for(timedelta(minutes=duration))
            await self.logchannel.send(embed=embedMsg(ctx, msg=f"**{member}** [{member.id}] was muted for {duration}"
                                                               " minute(s)."))
            await ctx.author.send(f"You have just muted {member}, remember to add a reason to the google sheets if "
                                  f"not given in the command.")
        except:
            await ctx.author.send("Cannot mute that member or you specified an invalid member.")
        await ctx.message.delete()

    @commands.command()
    @commands.has_role('Discord Moderation Team')
    async def unmute(self, ctx, member=None):
        if member is None:
            await ctx.author.send("Please specify a user to be unmuted.")
            await ctx.message.delete()
            return

        try:
            member = await discord.ext.commands.MemberConverter().convert(ctx, member)
            await member.remove_timeout()
            await self.logchannel.send(embed=embedMsg(ctx, msg=f"**{member}** [{member.id}] was unmuted")
            await ctx.author.send(f"You have just unmuted {member}")
        except:
            await ctx.author.send("Cannot unmute that member or you specified an invalid member.")
        await ctx.message.delete()

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member=None):
        if member is None:
            await ctx.author.send("Please specify a user to be banned.")
            await ctx.message.delete()
            return

        try:
            member = await discord.ext.commands.MemberConverter().convert(ctx, member)
            await ctx.guild.ban(member)
            await self.logchannel.send(embed=embedMsg(ctx, msg=f"**{member}** [{member.id}] was banned."))
            await ctx.author.send(
                f"You have just banned {member}, remember to add a reason to the google sheets if not given in the "
                f"command.")
        except:
            await ctx.author.send("Cannot ban that member or you specified an invalid member.")
        await ctx.message.delete()

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member=None):
        if member is None:
            await ctx.author.send("Please specify a user to be unbanned.")
            await ctx.message.delete()
            return

        try:
            member = await discord.ext.commands.MemberConverter().convert(ctx, member)
            await ctx.guild.unban(member)
            await self.logchannel.send(embed=embedMsg(ctx, msg=f"**{member}** [{member.id}] was unbanned."))
            await ctx.author.send(f"You have just unbanned {member}")
        except:
            await ctx.author.send("Cannot unban that member or you specified an invalid member.")
        await ctx.message.delete()

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member=None):
        if member is None:
            await ctx.author.send("Please specify a user to be kicked.")
            await ctx.message.delete()
            return

        try:
            member = await discord.ext.commands.MemberConverter().convert(ctx, member)
            await ctx.guild.kick(member)
            await self.logchannel.send(
                embed=embedMsg(ctx, msg=f'**{member}** [{member.id}] was kicked by **{ctx.message.author}**.'))
            await ctx.author.send(
                f"You have just kicked {member}, remember to add a reason to the google sheets if not given in the "
                f"command.")
        except:
            await ctx.author.send("Cannot kick member or you specified an invalid member.")
        await ctx.message.delete()

    @commands.command(aliases=['purge', 'clear'])
    @commands.has_guild_permissions(manage_messages=True)
    async def clean(self, ctx, number: int):
        await ctx.channel.purge(limit=number + 1)


def setup(bot):
    bot.add_cog(ModCommands(bot))
