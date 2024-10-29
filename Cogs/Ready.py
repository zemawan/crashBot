import Config
import disnake
import asyncio

from disnake.ext import commands

class Ready(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def updateUsers(self):
		for action, users in Config.deletedActions.items():
			for user, cases in list(users.items()):
				for case in list(cases):
					case -= 1
					if case <= 0:
						cases.remove(case)

				if not cases:
					del users[user]

	async def loop(self):
		while True:
			print(Config.deletedActions)
			await self.updateUsers()
			await asyncio.sleep(60)

	@commands.Cog.listener()
	async def on_ready(self):
		print("Бот готов к работе!")
		await self.loop()

def setup(bot):
	bot.add_cog(Ready(bot))