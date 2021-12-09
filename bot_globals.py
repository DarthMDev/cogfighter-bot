import discord
from discord.ext import commands
import sqlite_funcs as db
import json

# Global Variables
# Gag constants
GAG_EMOS = ('<:cupcake:914821822875316224>', '<:fruitpieslice:914821822812409898>',
            '<:creampieslice:914821822598512702>', '<:fruitpie:914821822875320330>', '<:creampie:914821822229405726>',
            '<:bday:914821822715936788>', '<:wedding:914821822632067152>')
GAGS = ('Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake')
GAG_DAMAGES = (5, 15, 25, 50, 75, 115, 165)

# Cog constants
SUIT_NAMES = (
'Cold Caller', 'Telemarketer', 'Name Dropper', 'Glad Hander', 'Mover and Shaker', 'Two Face', 'Mingler', 'Mr Hollywood')
SUIT_IMAGES = ('https://cdn.discordapp.com/attachments/917177481847521300/917177636676059146/262.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177733161832528/139.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177763243384922/203.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177804716638208/256.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177835016323072/189.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177864619700224/238.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177910073389056/248.png',
               'https://cdn.discordapp.com/attachments/917177481847521300/917177955287969812/244.png')

#Bot Variables
with open('config/config.json') as file:
    conf = json.load(file)
PREFIX = conf.get('prefix')
TOKEN = conf.get('token')
cogFighter = commands.Bot(command_prefix=PREFIX)


# Global Functions
def embedMsg(ctx, msg='', title='', url='', image=''):
    emb = discord.Embed(title = title, url=url, description= msg)
    emb.set_image(url=image)
    emb.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar.url)
    return emb

async def createAccount(ctx):
    if not db.does_user_exist(ctx.author.id):
        db.create_user(ctx.author.id)
        await ctx.send(embed=embedMsg(ctx, msg="Account Created!", title=''))