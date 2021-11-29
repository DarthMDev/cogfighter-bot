import sqlite3
from discord.ext import commands

con = sqlite3.connect('users.db')
cur = con.cursor()


# Takes the user's ID, and the amount of jelly beans to add to their balance and adds it to their balance.
def add_balance(id, num):
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    userBal = cur.fetchone()[1]
    userBal += num
    with con:
        cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': id})


def sub_balance(id, num):
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    userBal = cur.fetchone()[1]
    userBal -= num
    with con:
        cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': id})


def set_value(id, var, value):
    with con:
        cur.execute("UPDATE users SET {} = :value WHERE id = :id".format(var), {'value': value, 'id': id})


def create_user(id):
    with con:
        cur.execute("INSERT INTO users VALUES (:id, 100, 1, 0.0, 0.0, '[]')", {'id': id})


def fetch_data(id, var):
    if var == 'inventory':
        cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
        return cur.fetchone()[0].strip('][').split(', ')
    cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
    return cur.fetchone()[0]


def does_user_exist(id):
    cur.execute("SELECT * FROM users WHERE id = :id", {'id': id})
    if cur.fetchone() is None: return False
    else: return True

# Leaving the next comment here for future reference while this file is being worked on.
# cur.execute("CREATE TABLE users (id text, balance integer, crates integer, dailycooldown real, weeklycooldown real, inventory blob)")
