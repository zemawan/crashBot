import sqlite3
import string
import random

def generatePassword(length = 64):
    characters = string.ascii_letters + string.digits
    activationKey = ''.join(random.choice(characters) for _ in range(length))
    return activationKey

def createTable():
    connection = sqlite3.connect("Data/Database.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS servers (
        guild_id INTEGER PRIMARY KEY,
        password TEXT
    )''')

    connection.commit()

def addServerToDb(guildId):
    connection = sqlite3.connect("Data/Database.db")
    cursor = connection.cursor()
    password = generatePassword()
    cursor.execute("INSERT OR IGNORE INTO servers (guild_id, password) VALUES (?, ?)", (guildId, password))
    connection.commit()
    connection.close()

    return password

def removeServerFromDb(guildId):
    connection = sqlite3.connect("Data/Database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM servers WHERE guild_id=?", (guildId, ))
    connection.commit()
    connection.close()