from discord.ext import commands
import os
import json
import discord
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='&', intents=intents)

async def load_extensions():
	for filename in os.listdir("bot/cogs"):
		if filename.endswith(".py"):
			await client.load_extension(f"cogs.{filename[:-3]}")
			
async def main():
    async with client:
        await load_extensions()
        await client.start("OTczMDUwMDg1NTM5NzM3NjAw.GR-Bfq.UjJm14yphxG2NieVDV7Bd91qeX2npi0ULT2En8")

asyncio.run(main())