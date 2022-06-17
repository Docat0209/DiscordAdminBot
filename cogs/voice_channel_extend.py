from sys import flags
from discord.ext import commands
import discord
import json

path = ""
data = None

class VoiceChannelExtend(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		global data , path

		path = './data/voice_channel_extend.json'
		data = load_json(path)
		print("voice_channel_extend online")

	@commands.Cog.listener()
	async def on_voice_state_update(self,member, before, after):
		global data , path

		flags_after = True

		if after.channel == None:
			flags_after = False
		
		if(flags_after):
			category_id_after = str(after.channel.category.id)
			if(category_id_after not in data.keys()):
				flags_after = False

		if(flags_after):
			if(str(after.channel.id) != data[category_id_after]["channel_id"][len(data[category_id_after]["channel_id"])-1]):
				flags_after = False
		
		if(flags_after):
			channel = await after.channel.category.create_voice_channel(data[category_id_after]["channel_name"]+" - "+str(len(data[category_id_after]["channel_id"])+1))
			data[category_id_after]["channel_id"].append(str(channel.id))
			data = write_json(path,data)
		
			
		flags_before = True	

		if before.channel == None:
			flags_before = False

		if(flags_before):
			if(before.channel.members != []):
				flags_before = False

		if(flags_before):
			category_id_before = str(before.channel.category.id)
			if(category_id_before not in data.keys()):
				flags_before = False
	
		if(flags_before):
			for i in range(len(data[category_id_before]["channel_id"])-1)[::-1]:
				next_members = discord.Client.get_channel(self.client,int(data[category_id_before]["channel_id"][i+1])).members
				members = discord.Client.get_channel(self.client,int(data[category_id_before]["channel_id"][i])).members

				if(members == [] and next_members == []):
					await discord.Client.get_channel(self.client,int(data[category_id_before]["channel_id"][i+1])).delete()
					data[category_id_before]["channel_id"].pop(i+1)
					data = write_json(path,data)
				else:
					return



def setup(client):
	client.add_cog(VoiceChannelExtend(client))

def write_json(path ,data):

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()

    with open(path, encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    return (data)

def load_json(path):

    with open(path, 'r' , encoding="utf8") as f:
        data = json.load(f)

    return(data)
