from discord.ext import commands
import emoji
import discord
import re

class Test(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("test online")

	@commands.Cog.listener()
	async def on_voice_state_update(self,member, before, after):
		print(member , before ,after)
		print(after.channel.id)
		print(after.channel.category.id)
	


def setup(client):
	client.add_cog(Test(client))

def is_emoji(s):
    return s in emoji.UNICODE_EMOJI_ENGLISH

def is_discord_emoji(s):
	matched = re.match("^<:[a-z0-9_]+:[0-9]+>", s)
	return bool(matched)