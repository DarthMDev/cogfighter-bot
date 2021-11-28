import sqlite3
from discord.ext import commands

con = sqlite3.connect('users.db')
cur = con.cursor()

def add_balance(ctx, num):
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': ctx.author.id})
    userBal = cur.fetchone()[1]
    userBal += num
    cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': ctx.author.id})
    con.commit()

# Add Balance test, Passed!
# add_balance(1, 100)

def sub_balance(ctx, num):
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': ctx.author.id})
    userBal = cur.fetchone()[1]
    userBal -= num
    cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': ctx.author.id})
    con.commit()
    
def set_balance(ctx, num):
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': ctx.author.id})
    userBal = cur.fetchone()[1]
    userBal = num
    cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': ctx.author.id})
    con.commit()
 
# Subtract Balance test, Passed!
# sub_balance(1, 150)
