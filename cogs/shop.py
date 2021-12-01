import discord
from discord.ext import commands
from . import sqliteFuncs as db

class Shop(commands.Cog):
    def __init__(self, bot):
        #initial variables
        self.bot = bot
        self.items = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']
        self.prices = [10, 20, 30, 40, 50, 60, 70]

    @commands.command()
    async def shop(self, ctx):
        message = "List of shop items:"
        message += "\n"
        for x in self.getItems():
            index = self.getIndexofItem(x)
            message += "{0} : {1} jellybeans ".format(x, self.getPriceofItem(index))
        await ctx.send(message) 

    def getIndexofItem(self, item):
        """
        Gets the index of an item using the list of items in the shop
        """
        index = self.getItems().index(item)
        return int(index)

    def getPriceofItem(self, index):
        """

        Gets the price of an item using the index provided
        """
        return self.getPrices()[index]

    @commands.command(pass_context = True)
    async def buy(self, ctx, item):
        indexNumber = None
        for x in self.getItems():
            if self.getItems()[x] == item:
                indexNumber = x
        price = self.getPriceofItem(indexNumber)
        if db.fetch_data(ctx.author.id, 'balance') < price :
            await ctx.send('You do not have enough jellybeans.')
            return
        else:
            return
            #TODO Make compatible with adding a new gag in the new inventory system
            db.sub_balance(ctx.author.id, price)
            await ctx.send("Successfully purchased {0} for {1} jellybeans.".format(str(item), str(price) ))
            return
    def setItems(self, items):
        """
        Sets the list of items in the shop 
        """
        self.items = items

    def getItems(self):
        """
        Gets the list of items in the shop
        """
        return self.items

    def setPrices(self, prices):
        """
        Sets the list of prices in the shop, 
        the indexes should correspond with that of items
        """
        self.prices = prices

    def getPrices(self):
        """
        Gets the list of prices in the shop
        """
        return self.prices

def setup(bot):
    bot.add_cog(Shop(bot))