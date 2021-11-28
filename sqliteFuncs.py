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

# Subtract Balance test, Passed!
# sub_balance(1, 150)

def set_balance(id, num):
    cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': num, 'id': id})
    con.commit()

# Set Balance test, Passed!
# set_balance(1, 7905)

def create_user(ctx, startingBal):
    cur.execute("INSERT INTO users VALUES (:id, :startingBal)", {'id': ctx.author.id, 'startingBal': startingBal})
    con.commit()

# Create user test, Passed!
# create_user(2, 39)