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


def add_cooldown(id, num):
    #TODO create entry for author cooldown for the event then we can make these functions
    pass #TODO


def sub_cooldown(id, num):
    pass #TODO


def set_value(id, var, value):
    """
    Takes the user's id, the variable you want to set, and the value to set it to.
    vars: balance, crates, dailycooldown, weeklycooldown, inventory
    value: For balance and crates, Int. for dailycooldoqn and weeklycooldown, Float. For inventory, List
    """
    if var == 'inventory':
        commit = []
        for i in value:
            commit.append(i.strip("{}{}".format('"', "'")))
        commit = str(commit)
        with con:
            cur.execute("UPDATE users SET {} = :commit WHERE id = :id".format(var), {'commit': commit, 'id': id})
        return
    with con:
        cur.execute("UPDATE users SET {} = :value WHERE id = :id".format(var), {'value': value, 'id': id})

def fetch_data(id, var):
    """
    Fetches data based on the id and which variable you want.
    Supported vars: balance, crates, dailycooldown, weeklycooldown, inventory
    """
    if var == 'inventory':
        cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
        x = cur.fetchone()[0].strip("[]").split(', ')
        y = []
        for i in x: y.append(i.strip("{}{}".format("'", '"')))
        return y
    cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
    return cur.fetchone()[0]


def create_user(id):
    """
    Creates a new user in the database based on the id specified
    default values:
    balance: 100, crates: 0, dailycooldown: 0, weeklycooldown: 0, inventory: '[]'
    """
    #TODO in the future make it so if no id is specified make
    # it so its based on the last id number in the database +1 
    #I think it should be something built into sql but not sure
    with con:
        cur.execute("INSERT INTO users VALUES (:id, 100, 0, 0.0, 0.0, '[]')", {'id': id})


def remove_user(id):
    with con:
        cur.execute("DELETE from users where id = :id", {'id': id})


def does_user_exist(id):
    """
    Function that checks if a user exists based on the id specified
    """
    cur.execute("SELECT * FROM users WHERE id = :id", {'id': id})
    if cur.fetchone() is None: return False
    else: return True


# Leaving the next comment here for future reference while this file is being worked on.
# cur.execute("CREATE TABLE users (id integer, balance integer, crates integer, dailycooldown real, weeklycooldown real, inventory text)")
