from discord.ext import commands
import os
import json
import discord
from alive_progress import alive_bar

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='&', intents=intents)


toolbar_width = 0
for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		toolbar_width = toolbar_width + 1

print(f"Loding cogs ({toolbar_width} items)")

with alive_bar(toolbar_width) as bar:
	for f in os.listdir("./cogs"):
		if f.endswith(".py"):
			client.load_extension("cogs." + f[:-3])
			bar()

with open('./data/token.json', 'r') as f:
	data = json.load(f)

client.run(data['token'])