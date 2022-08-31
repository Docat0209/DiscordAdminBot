from discord.ext import commands
import emoji
import discord
import re
from discord import RawReactionActionEvent
import json
import asyncio

path = ""
data = None

class EventHost(commands.Cog):
    
    def __init__(self, client):
        self.client = client # sets the client variable so we can use it in cogs'
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        global data , path

        path = './data/event_host.json'
        data = load_json(path)
        print("event_host online")

    #---互動表情新增選擇---
    @commands.Cog.listener()
    async def on_raw_reaction_add(self , payload: RawReactionActionEvent):
        global data , path

        if str(payload.message_id) not in data:
            return
        
        if str(payload.emoji) == "✅":
            data[str(payload.message_id)]["members"].append(str(payload.user_id))
            data = write_json(path,data)

            embed = refresh_embed(data , payload.message_id)

            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.edit(embed=embed)

        if len(data[str(payload.message_id)]["members"]) >= int(data[str(payload.message_id)]["goal"]):

            embed = refresh_embed(data , payload.message_id)

            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.edit(embed=embed)

            data.pop(str(payload.message_id),None)
            data = write_json(path,data)
            return     

            
    #---互動表情移除選擇---
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self , payload: RawReactionActionEvent):
        global data , path

        if str(payload.message_id) not in data:
            return

        if str(payload.emoji) == "✅":
            data[str(payload.message_id)]["members"].remove(str(payload.user_id))
            data = write_json(path,data)

            embed = refresh_embed(data , payload.message_id)

            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.edit(embed=embed)


    #---主持活動---
    @commands.command()
    async def event_host(self, ctx, title ,goal:int , time:int):
        global data , path

        if goal <= 0:
            await ctx.send("wrong format")
            await ctx.message.delete()
            return

        embed=discord.Embed(title="參加活動", description= "活動生成中",color=0x2ecc71)

        message = await ctx.send(embed=embed)

        await message.add_reaction("✅")

        message_id = message.id

        if message_id not in data:
            data.update({str(message_id):{"title":title,"time":time,"goal":goal,"members":[]}})
            data = write_json(path,data)
        
        await ctx.message.delete()

        while (1):
            if(data[str(message_id)]["time"] == 0):
                message = await ctx.fetch_message(message_id)

                embed = refresh_embed(data , message_id , True)

                await message.edit(embed=embed)
                data.pop(str(message_id),None)
                data = write_json(path,data)
                break

            else:
                message = await ctx.fetch_message(message_id)

                embed = refresh_embed(data , message_id)

                await message.edit(embed=embed)
                data[str(message_id)].update({"time":data[str(message_id)]["time"]-1})
                data = write_json(path,data)

                await asyncio.sleep(3600)


def refresh_embed(data , message_id , timeout = False):
    join_members = ""
    for i in data[str(message_id)]["members"]:
        join_members = join_members + f"<@{i}>\n"

    if join_members == "":
        join_members = "尚未有人加入"

    embed=discord.Embed(title="參加活動", description="" ,color=0x2ecc71)
    embed.add_field(name="活動名稱", value=data[str(message_id)]["title"] , inline=False)
    embed.add_field(name="目標人數", value=data[str(message_id)]["goal"] , inline=True)
    time_string = "`"+str(int(int(data[str(message_id)]["time"]/24)))+"`天`"+str(int(data[str(message_id)]["time"])%24)+"`小時"
    if int(int(data[str(message_id)]["time"]/24)) + int(data[str(message_id)]["time"])%24 == 0:
        time_string = "小於1小時"

    if timeout:
        time_string = "已超時"

    embed.add_field(name="剩餘時間", value= time_string , inline=True)
    embed.add_field(name="目前參與人員", value=join_members , inline=False)

    return embed


async def setup(client):
    await client.add_cog(EventHost(client))

def is_emoji(s):
    return s in emoji.UNICODE_EMOJI_ENGLISH

def is_discord_emoji(s):
	matched = re.match("^<:[a-z0-9_A-Z]+:[0-9]+>", s)
	return bool(matched)

def is_discord_role(s):
	matched = re.match("^<@&[0-9]+>", s)
	return bool(matched)
    

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