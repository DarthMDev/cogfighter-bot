import sqlite3
from discord.ext import commands

con = sqlite3.connect('users.db')
cur = con.cursor()
gags = ['Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Fruit Pie', 'Cream Pie', 'Birthday Cake', 'Wedding Cake']


def bal(id: int) -> int:
    """
    takes the user id and returns their balance as a int
    """
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    return cur.fetchone()[1]


# Takes the user's ID, and the amount of jelly beans to add to their balance and adds it to their balance.
def add_balance(id: int, num: int):
    """
    A function that takes a user's id and a number
    and adds that number to their balance.
    """
    userBal = bal(id)
    userBal += num
    with con:
        cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': id})


def sub_balance(id: int, num: int):
    """
        A function that takes a user's id and a number
        and subtracts that number from their balance.
    """
    userBal = bal(id)
    userBal -= num
    with con:
        cur.execute("UPDATE users SET balance = :bal WHERE id = :id", {'bal': userBal, 'id': id})


def add_crates(id: int, num: int):
    """
        A function that takes a user's id and a number and adds that number
         to the amount of crates they have.
    """
    cur.execute("SELECT * FROM users  WHERE id = :id", {'id': id})
    userCrates = cur.fetchone()[2]
    userCrates += num
    with con:
        cur.execute("UPDATE users SET crates = :bal WHERE id = :id", {'bal': userCrates, 'id': id})


def sub_crates(id: int, num: int) -> None:
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
    # TODO create entry for author cooldown for the event then we can make these functions
    pass  # TODO


def sub_cooldown(id, num):
    pass  # TODO


def set_value(id: int, var: str, value: any) -> None:
    """
    Takes the user's id, the variable you want to set, and the value to set it to.
    vars: balance, crates, dailycooldown, weeklycooldown, inventory
    value: For balance and crates, Int. for dailycooldoqn and weeklycooldown, Float. For inventory, List
    """
    if var == 'inventory':
        # creates an iterator that performs the str function on every item in value, then separates each value with a space
        iterator = map(str, value)
        y = " ".join(list(iterator))
        with con:
            cur.execute("UPDATE users SET {} = :value WHERE id = :id".format(var), {'value': y, 'id': id})
        return
    with con:
        cur.execute("UPDATE users SET {} = :value WHERE id = :id".format(var), {'value': value, 'id': id})


def fetch_data(id: int, var: str) -> any:
    """
    Fetches data based on the id and which variable you want.
    Supported vars: balance, crates, dailycooldown, weeklycooldown, inventory
    """
    if var == 'inventory':
        cur.execute("SELECT inventory FROM 'users' WHERE id = :id", {'id': id})
        return list(map(int, cur.fetchone()[0].split(' ')))
    cur.execute("SELECT {} FROM 'users' WHERE id = :id".format(var), {'id': id})
    return cur.fetchone()[0]


def add_item(id: int, item: str, num: int=1) -> None:

    inv = fetch_data(id, 'inventory')
    index = gags.index(item)
    inv[index] += num
    set_value(id, 'inventory', inv)


def sub_item(id: int, item: str, num: int=1) -> None:

    inv = fetch_data(id, 'inventory')
    index = gags.index(item)
    inv[index] -= num
    if inv[index] < 0:
        inv[index] = 0
    set_value(id, 'inventory', inv)


def create_user(id: int) -> None:
    """
    Creates a new user in the database based on the id specified
    default values:
    balance: 100, crates: 0, dailycooldown: 0, weeklycooldown: 0, inventory: '[]'
    """
    with con:
        cur.execute("INSERT INTO users VALUES (:id, 100, 0, 0.0, 0.0, '0 0 0 0 0 0 0')", {'id': id})


def remove_user(id: int) -> None:
    with con:
        cur.execute("DELETE from users where id = :id", {'id': id})


def does_user_exist(id: int) -> bool:
    """
    Function that checks if a user exists based on the id specified
    """
    cur.execute("SELECT * FROM users WHERE id = :id", {'id': id})

    # turning None into a boolean makes it false, whereas for any other variable it makes it true
    return bool(cur.fetchone())

# Leaving the next comment here for future reference while this file is being worked on.
# cur.execute("CREATE TABLE users (id integer, balance integer, crates integer, dailycooldown real, weeklycooldown real, inventory text)")