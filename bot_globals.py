import discord

# Global Variables
# Gag constants
GAG_EMOS = ['<:cupcake:914821822875316224>', '<:fruitpieslice:914821822812409898>',
            '<:creampieslice:914821822598512702>', '<:fruitpie:914821822875320330>', '<:creampie:914821822229405726>',
            '<:bday:914821822715936788>', '<:wedding:914821822632067152>']
GAGS = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']
THROW_DAMAGES = [5, 15, 25 , 50, 75, 115, 165, 225, 295, 375]

# Cog constants

#Global Functions
def embedMsg(ctx, msg, title='', url='', image=''):
    emb = discord.Embed(title = title, url=url, description= msg)
    emb.set_image(url=image)
    emb.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    return emb