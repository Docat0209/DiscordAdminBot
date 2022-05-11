from discord.ext import commands

class Test(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("on_ready")
	
	@commands.command()
	async def command(self, ctx , list:list):
		print(list)
		await ctx.message.delete()


def setup(client):
	client.add_cog(Test(client))