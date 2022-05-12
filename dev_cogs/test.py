from discord.ext import commands
import emoji
import discord
import re

class Test(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("on_ready")
	
	@commands.command()
	async def command(self, ctx ):
		print(ctx.message.reference)
		if ctx.message.reference is not None  :
			print("True")



def setup(client):
	client.add_cog(Test(client))

def is_emoji(s):
    return s in emoji.UNICODE_EMOJI_ENGLISH

def is_discord_emoji(s):
	matched = re.match("^<:[a-z0-9_]+:[0-9]+>", s)
	return bool(matched)