import Config
import disnake
import asyncio

from disnake.ext import commands

class Ready(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def updateUsers(self):
	    for actionId, actionData in Config.deletedActions.items():
	        for actionType, users in actionData.items():
	            for user, cases in list(users.items()):
	                for i, case in enumerate(cases):
	                    cases[i] -= 1
	                    if cases[i] <= 0:
	                        del cases[i]

	                if not cases:
	                    del users[user]

	async def loop(self):
		while True:
			await self.updateUsers()
			await asyncio.sleep(60)

	@commands.Cog.listener()
	async def on_ready(self):
		print("Бот готов к работе!")
		await self.loop()

def setup(bot):
	bot.add_cog(Ready(bot))
