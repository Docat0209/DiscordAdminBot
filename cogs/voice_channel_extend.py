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
				members = discord.Client.get_channel(self.client,int(data[category_id_before]["channel_id"][i])).members
				if(members == []):
					channel_id = data[category_id_before]["channel_id"][i]
					data[category_id_before]["channel_id"].pop(i)
					data = write_json(path,data)
					await discord.Client.get_channel(self.client,int(channel_id)).delete()
					
			for i in range(len(data[category_id_before]["channel_id"]))[::-1]:
				channel_id = data[category_id_before]["channel_id"][i]
				await discord.Client.get_channel(self.client,int(channel_id)).edit(name=data[category_id_before]["channel_name"]+" - "+str(data[category_id_before]["channel_id"].index(channel_id)+1))



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
