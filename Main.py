import Database

from os import getenv
from dotenv import load_dotenv
from Utils import CrashBot

Database.createTable()
load_dotenv()

bot = CrashBot()
bot.loadCog("Cogs")
bot.run(getenv("TOKEN"))