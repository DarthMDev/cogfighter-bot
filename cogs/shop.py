from cogFighter.bot_globals import *

PRICES = [10, 20, 30, 40, 50, 60, 70]

class Shop(commands.Cog):

    def __init__(self, bot):
        # initial variables
        self.bot = bot
        self.items = GAGS
        self.prices = PRICES
        self.emojis = GAG_EMOS

    @commands.command(aliases=['gagshop', 'store'])
    async def shop(self, ctx):
        title = "Shop"
        message = "List of shop items:"
        for x in self.items:
            index = self.getIndexofItem(x)
            message += f"\n{self.emojis[index]} {x} : {self.getPriceofItem(index)} jellybeans"
        await ctx.send(embed=embedMsg(ctx, msg=message, title=title))


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
        title = ''
        if not db.does_user_exist(ctx.author.id):
            db.create_user(ctx.author.id)
            await ctx.send("Account created")

        # args is the item the user wants
        item = " ".join(args)
        try:
            indexNumber = self.getIndexofItem(item.title())
            price = self.getPriceofItem(indexNumber)
        except ValueError:
            title = "Error"
            await ctx.send(embed=embedMsg(ctx, msg="Item does not exist in shop!", title=title))
            return
        if db.fetch_data(ctx.author.id, 'balance') < price:
            title = 'Error'
            await ctx.send(embed=embedMsg(ctx, msg='You do not have enough jellybeans.', title=title))
            return
        else:
            db.add_item(ctx.author.id, item.title())
            title = 'Success'
            db.sub_balance(ctx.author.id, price)
            await ctx.send(embed=embedMsg(ctx,
                                          msg=f"Successfully purchased {str(item.title())} for {str(price)} jellybeans.",
                                          title=title))
            return


def setup(bot):
    bot.add_cog(Shop(bot))
