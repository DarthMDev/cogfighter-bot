import discord
from discord.ext import commands
import sqliteFuncs as db


class Shop(commands.Cog):
    def __init__(self, bot):
        # initial variables
        self.bot = bot
        self.items = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']
        self.prices = [10, 20, 30, 40, 50, 60, 70]
        self.emojis = ['<:cupcake:914821822875316224>', '<:fruitpieslice:914821822812409898>', '<:creampieslice:914821822598512702>', '<:fruitpie:914821822875320330>', '<:creampie:914821822229405726>', '<:bday:914821822715936788>', '<:wedding:914821822632067152>']

    @commands.command(aliases=['gagshop', 'store'])
    async def shop(self, ctx):
        message = "List of shop items:"
        message += "\n"
        for x in self.items:
            index = self.getIndexofItem(x)
            message += f"{self.emojis[index]} {x} : {self.getPriceofItem(index)} jellybeans \n"
        await ctx.send(message)

    def getIndexofItem(self, item):
        """
        Gets the index of an item using the list of items in the shop
        """
        index = self.items.index(item)
        return int(index)

    def getPriceofItem(self, index):
        """
        Gets the price of an item using the index provided
        """
        return self.prices[index]

    @commands.command(aliases=['purchase'], pass_context=True)
    async def buy(self, ctx, *args):

        if not db.does_user_exist(ctx.author.id):
            db.create_user(ctx.author.id)
            await ctx.send("Account created")

        # args is the item the user wants
        item = " ".join(args)
        try:
            indexNumber = self.getIndexofItem(item.title())
            price = self.getPriceofItem(indexNumber)
        except ValueError:
            await ctx.send("Item does not exist in shop!")
            return
        if db.fetch_data(ctx.author.id, 'balance') < price:
            await ctx.send('You do not have enough jellybeans.')
            return
        else:
            db.add_item(ctx.author.id, item.title())
            db.sub_balance(ctx.author.id, price)
            await ctx.send(f"Successfully purchased {str(item.title())} for {str(price)} jellybeans.")
            return


def setup(bot):
    bot.add_cog(Shop(bot))
