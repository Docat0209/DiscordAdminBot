from discord.ext import commands
import os
import json
import discord

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='&', intents=intents)


for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension("cogs." + f[:-3])

with open('./data/token.json', 'r') as f:
    data = json.load(f)

client.run(data['token'])