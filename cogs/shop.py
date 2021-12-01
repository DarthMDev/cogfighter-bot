import discord
from discord.ext import commands
import sqliteFuncs as db

class Shop(commands.Cog):
    def __init__(self, bot):
        #initial variables
        self.bot = bot
        self.items = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']
        self.prices = [10, 20, 30, 40, 50, 60, 70]
        self.emojis = ['<:cupcake:914821822875316224>', '<:fruitpieslice:914821822812409898>', '<:creampieslice:914821822598512702>', '<:fruitpie:914821822875320330>', '<:creampie:914821822229405726>', '<:bday:914821822715936788>', '<:wedding:914821822632067152>']
   
    @commands.command(aliases=['gagshop', 'store'])
    async def shop(self, ctx):
        message = "List of shop items:"
        message += "\n"
        for x in self.getItems():
            index = self.getIndexofItem(x)
            message += "{0} {1} : {2} jellybeans \n".format(self.getEmojiofItem(index), x, self.getPriceofItem(index))
        await ctx.send(message) 

    def getEmojiofItem(self, index):
        return self.getEmojis()[index]

    def getEmojis(self):
        return self.emojis

    def setEmojis(self, emojis):
        self.emojis = emojis

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

    @commands.command(aliases=['purchase'], pass_context = True)
    async def buy(self, ctx, *args ):

        if not db.does_user_exist(ctx.author.id):
            db.create_user(ctx.author.id)
            await ctx.send("Account created")
        #args is the item the user wants
        item = (" ".join(args[:]))
        try:
            indexNumber = self.getIndexofItem(item)
            price = self.getPriceofItem(indexNumber)
        except:
            await ctx.send("Item doesn't exist in shop , remember items are case sensitive and to not include  the emoji.")
            return 
        if db.fetch_data(ctx.author.id, 'balance') < price :
            await ctx.send('You do not have enough jellybeans.')
            return
        else:
            db.add_item(ctx.author.id, item)
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