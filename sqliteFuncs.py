import sqlite3
from discord.ext import commands

con = sqlite3.connect('users.db')
cur = con.cursor()


# Takes the user's ID, and the amount of jelly beans to add to their balance and adds it to their balance.
def add_balance(id, num):
    """

    A function that takes a user's id and a number 
    and adds that number to their balance.
    """
    #reads database and gets the specified user's data
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    #Fetches the balance of the specified user
    userBal = cur.fetchone()[1]
    #Adds the amount specified in the argument to the varuable
    userBal += num
    with con:
        #Updates the user's balance , based on the id an the variable we assigned
        cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': id})


def sub_balance(id, num):
    """
        A function that takes a user's id and a number 
        and subtracts that number from their balance.

    """
    #reads database and gets the specified user's data

    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    #Fetches the balance of the specified user
    userBal = cur.fetchone()[1]
    #Subtracts the amount specified in the argument to the varuable
    userBal -= num
    with con:
        #Updates the user's balance , based on the id an the variable we assigned
        cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': id})


def add_crates(id, num):
    """
        A function that takes a user's id and a number and adds that number
         to the amount of crates they have.

    """
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    userCrates = cur.fetchone()[2]
    userCrates += num
    with con:
        cur.execute("UPDATE users SET crates = :bal WHERE id = :id", {'bal': userCrates, 'id': id})


def sub_crates(id, num):
    """
        A function that takes a user's id and a number and subtracts that number
         from the amount of crates they have.

    """
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    userCrates = cur.fetchone()[2]
    userCrates -= num
    with con:
        cur.execute("UPDATE users SET crates = :bal WHERE id = :id", {'bal': userCrates, 'id': id})


def set_value(id, var, value):
    with con:
        cur.execute("UPDATE users SET {} = :value WHERE id = :id".format(var), {'value': value, 'id': id})


def create_user(id):
    """
    Creates a new user in the database based on the id specified
    """
    #TODO in the future make it so if no id is specified make
    # it so its based on the last id number in the database +1 
    #I think it should be something built into sql but not sure
    with con:
        cur.execute("INSERT INTO users VALUES (:id, 100, 1, 0.0, 0.0, '[]')", {'id': id})


def fetch_data(id, var):
    """
    Fetches data based on the id and  type of data you want.
    Current list of options for var: [inventory]
    """
    if var == 'inventory':
        cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
        return cur.fetchone()[0].strip('][').split(', ')
    cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
    return cur.fetchone()[0]


def does_user_exist(id):
    """
    Function that checks if a user exists based on the id specified
    """
    cur.execute("SELECT * FROM users WHERE id = :id", {'id': id})
    if cur.fetchone() is None: return False
    else: return True

# Leaving the next comment here for future reference while this file is being worked on.
# cur.execute("CREATE TABLE users (id integer, balance integer, crates integer, dailycooldown real, weeklycooldown real, inventory blob)")
