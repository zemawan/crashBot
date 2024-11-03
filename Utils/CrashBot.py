import disnake
import os

from disnake.ext import commands

class CrashBot(commands.InteractionBot):
	def __init__(self):
		super().__init__(
			intents = disnake.Intents.all(),
		)

	def loadCog(self, path: str):
		for root, _, files in os.walk(path):
			for file in files:
				if not file.endswith(".py"):
					continue

				path = os.path.join(root, file)
				extension = path.replace("/", ".").replace("\\", ".")[:-3]

				try:
					self.load_extension(extension)
					print(f"Ког {extension} успешно загружен.")
				except Exception as e:
					print(f"Не удалось загрузить ког {extension}: {e}.")