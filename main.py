from discord.ext import commands
import os
import json
import discord
import asyncio
from alive_progress import alive_bar

async def load_extensions():
	with alive_bar(toolbar_width) as bar:
		for filename in os.listdir("./cogs"):
			if filename.endswith(".py"):
				await client.load_extension(f"cogs.{filename[:-3]}")
				bar()
			
async def main():
    async with client:
        await load_extensions()
        await client.start("")

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='&', intents=intents)

toolbar_width = 0
for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		toolbar_width = toolbar_width + 1

print(f"Loding cogs ({toolbar_width} items)")

asyncio.run(main())