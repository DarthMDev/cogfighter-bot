import sys
sys.path.append("..")
import random
from bot_globals import *


class SuitFight(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.damages = GAG_DAMAGES
        self.suitNames = SUIT_NAMES
        self.suit = ''
        self.suitHealth = 0
        self.suitLevel = 0
        self.message = None
        self.thread = None
        self.suitMaxHealth = 0
        self.participants = []
        self.channel = cogFighter.get_channel(813541240003887142)


    def healthEmoji(self):
        ratio = self.suitHealth/self.suitMaxHealth
        if ratio > 0.75:
            return "🟢"
        elif ratio > 0.5:
            return "🟡"
        elif ratio > 0.25:
            return "🟠"
        elif ratio > 0:
            return "🔴"
        else:
            return "⚫"


    @commands.command()
    async def startFight(self, ctx):
        self.suitLevel = int(random.randint(1, 25))
        if self.suitLevel == 1 or self.suitLevel == 2:
            self.suit = SUIT_NAMES[0]
        elif self.suitLevel == 3 or self.suitLevel == 4:
            self.suit = SUIT_NAMES[random.randint(0,1)]
        elif self.suitLevel == 5:
            self.suit = SUIT_NAMES[random.randint(0,2)]
        elif self.suitLevel == 6:
            self.suit = SUIT_NAMES[random.randint(1, 2)]
        elif self.suitLevel == 7:
            self.suit = SUIT_NAMES[random.randint(1, 3)]
        elif self.suitLevel == 8:
            self.suit = SUIT_NAMES[random.randint(2, 3)]
        elif self.suitLevel == 9 or self.suitLevel == 10:
            self.suit = SUIT_NAMES[random.randint(2, 4)]
        elif self.suitLevel == 11:
            self.suit = SUIT_NAMES[random.randint(3, 4)]
        elif self.suitLevel == 12 or self.suitLevel == 13:
            self.suit = SUIT_NAMES[random.randint(3, 5)]
        elif self.suitLevel == 14 or self.suitLevel == 15:
            self.suit = SUIT_NAMES[random.randint(4, 6)]
        elif self.suitLevel == 16:
            self.suit = SUIT_NAMES[random.randint(4, 7)]
        elif self.suitLevel == 17 or self.suitLevel == 18 or self.suitLevel == 19:
            self.suit = SUIT_NAMES[random.randint(5, 7)]
        elif self.suitLevel == 20 or self.suitLevel == 21 or self.suitLevel == 22:
            self.suit = SUIT_NAMES[random.randint(6, 7)]
        else:
            self.suit = SUIT_NAMES[7]

        self.suitMaxHealth = (self.suitLevel + 1) * (self.suitLevel + 2) * 3
        self.suitHealth = self.suitMaxHealth
        self.channel = await discord.ext.commands.GuildChannelConverter().convert(ctx, '813541240003887142')
        cogEmbed = discord.Embed(title=f"A level {self.suitLevel} {self.suit} has appeared!")
        cogEmbed.set_image(url=SUIT_IMAGES[SUIT_NAMES.index(self.suit)])
        cogEmbed.add_field(name="Cog HP", value=f"{self.healthEmoji()} {self.suitHealth}/{self.suitMaxHealth}")
        self.message = await self.channel.send(embed=cogEmbed)
        self.thread = await self.message.create_thread(name=f"{self.suit}")

        await self.thread.send(f"To damage the cog, use `{PREFIX}gag`, and then the gag name.")


    @commands.command()
    async def gag(self, ctx, *, gag):
        if ctx.channel != self.thread:
            return

        if not db.does_user_exist(ctx.author.id):
            ctx.send(embed=embedMsg(ctx, msg="Heya! Looks like you're a new toon. Explore the bot in the other playing "
                                             "channels and gather some gags before you try to fight a cog!"))
            return

        gag = gag.title()
        if gag in GAGS:
            index = GAGS.index(gag)
        else:
            await ctx.send(embed=embedMsg(ctx, msg="Not a valid gag!"))
            return

        inventory = db.fetch_data(ctx.author.id, 'inventory')
        if inventory[index] == 0:
            await ctx.send(embed=embedMsg(ctx, msg=f"You do not have a {gag}!"))
            return
        else:
            inventory[index] -= 1
            db.set_value(ctx.author.id, 'inventory', inventory)

        self.suitHealth -= GAG_DAMAGES[index]
        await ctx.send(embed=embedMsg(ctx, msg=f"You used a {gag} and dealt {str(GAG_DAMAGES[index])} damage!"))

        if not ctx.author in self.participants:
            self.participants.append(ctx.author)

        if self.suitHealth <= 0:
            await self.thread.delete()
            self.suitHealth = 0
            players = []

            if len(self.participants) == 1:
                players = self.participants[0].name
            else:
                for i in range(len(self.participants)-1):
                    players.append(self.participants[i].name)
                players = ", ".join(players)
                players += f" and {self.participants[-1].name}"

            reward = (int(self.suitLevel)**2) + (10 * int(self.suitLevel))
            await self.channel.send(embed=discord.Embed(title=f"Cog defeated! {players} received {reward} Jellybeans!"))
            for i in self.participants:
                db.add_balance(i.id, reward)
            self.participants = []

        newEmbed = discord.Embed(title=f"A level {self.suitLevel} {self.suit} appeared!")
        newEmbed.set_image(url=SUIT_IMAGES[SUIT_NAMES.index(self.suit)])
        newEmbed.add_field(name="Cog HP", value=f"{self.healthEmoji()} {self.suitHealth}/{self.suitMaxHealth}")
        await self.message.edit(embed=newEmbed)


def setup(bot):
    bot.add_cog(SuitFight(bot))
