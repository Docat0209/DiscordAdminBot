from discord.ext import commands
import discord
import random

class RandomTeam(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("random_team online")

	@commands.command()
	async def random_team(self, ctx , *arg):
		
		name_list = list(arg)

		random.shuffle(name_list)

		team1 = ""
		team2 = ""

		for i in range(len(name_list)):
			if i <= len(name_list)/2 - 1:
				team1 = team1 + name_list[i] + '\n'
			else:
				team2 = team2 + name_list[i] + '\n'
		
		embed=discord.Embed(title="隨機分隊", description="",color=0x2ecc71)
		embed.add_field(name="隊伍一", value=team1 , inline=True)
		embed.add_field(name="隊伍二", value=team2 , inline=True)
		await ctx.send(embed=embed)
		await ctx.message.delete()
	
def setup(client):
	client.add_cog(RandomTeam(client))
