from discord.ext import commands
import os

client = commands.Bot(command_prefix = "!")

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension("cogs." + f[:-3])

client.run("OTczMDUwMDg1NTM5NzM3NjAw.GP1i4Z.Jl7hwkqX803LASe8MSsnK8PjDYRceGT-vZqKS4")