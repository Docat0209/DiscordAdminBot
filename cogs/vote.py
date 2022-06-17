from enum import Flag
from turtle import color
import discord
import json
import asyncio
from discord.ext import commands
from discord import RawReactionActionEvent
import emoji
import re


path = ""
data = None

class Vote(commands.Cog):

    def __init__(self, client):
        self.client = client # sets the client variable so we can use it in cogs'
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        global data , path
        path = './data/vote.json'
        data = load_json(path)
        print("vote online")

    @commands.command()
    async def vote(self, ctx, title , time:int ,*arg):
        global data , path

        #---Check format---
        if time <= 0:
            await ctx.send("wrong format")
            await ctx.message.delete()
            return

        if len(arg)%2 != 0:
            await ctx.send("wrong format")
            await ctx.message.delete()
            return
        
        for i in range(int(len(arg)/2)):
            if(not (is_emoji(arg[i*2]) or is_discord_emoji(arg[i*2])) ):
                await ctx.send("wrong format")
                await ctx.message.delete()
                return

        #---Send vote message---
        embed=discord.Embed(title="", description="尚未啟用的投票" ,color=0x2ecc71)

        message = await ctx.send(embed=embed)

        message_id = message.id

        #---Save vote data to json---
        if message_id not in data:
            data.update({str(message_id):{}})
            data = write_json(path,data)

        data[str(message_id)].update({"time":time})
        data = write_json(path,data)
        
        for i in range(int(len(arg)/2)):
            data[str(message_id)].update({arg[i*2]:arg[i*2+1]})
            data = write_json(path,data)
            await message.add_reaction(arg[i*2])
        
        await ctx.message.delete()

        #---Time Listener---
        while (1):
            #---Get data---
            try:
                data
            except NameError:
                path = './data/vote.json'
                data = load_json(path)

            #---Check data---
            if(data[str(message_id)]["time"] == 0):
                #---Vote result---
                message = await ctx.fetch_message(message_id)
                h_emoji = ""
                h_count = 0

                for i in data[str(message_id)].keys():
                    if str(i) == "time":
                        continue
                    
                    if is_discord_emoji(i):
                        i =  discord.ext.commands.Bot.get_emoji(i.split(":")[2][:-1])
                    reaction = discord.utils.get(message.reactions, emoji=i)

                    if reaction.count > h_count:
                        h_count = reaction.count
                        h_emoji = i
                    elif reaction.count == h_count:
                        h_emoji = h_emoji +"#"+ i

                string = "**投票**\n"+title+"\n\n**結果**\n"

                for i in h_emoji.split("#"):
                    string = string + data[str(message_id)][i] +f" 獲得最高票"+ "\n"

                embed=discord.Embed(title="", description= string ,color=0x2ecc71)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
                data.pop(str(message_id),None)
                data = write_json(path,data)
                break

            else:
                #---Update data---
                string = "**投票**\n"+title+"\n\n**選項**\n"
                for i in range(int(len(arg)/2)):
                    string = string + arg[i*2] + "：" + arg[i*2+1] + "\n"

                string = string + "\n**相關資訊**\n⏰  投票剩餘 `"+str(int(int(data[str(message_id)]["time"]/24)))+"天"+str(int(data[str(message_id)]["time"])%24)+"小時`"
                embed=discord.Embed(title="", description=string ,color=0x2ecc71)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

                await message.edit(embed=embed)

                data[str(message_id)].update({"time":data[str(message_id)]["time"]-1})
                data = write_json(path,data)

                await asyncio.sleep(3600)


    #---報錯區域---
    @vote.error
    async def roles_error(self, ctx, error):
        await ctx.send(error)



def setup(client):
    client.add_cog(Vote(client))

def is_emoji(s):
    return s in emoji.UNICODE_EMOJI_ENGLISH

def is_discord_emoji(s):
	matched = re.match("^<:[a-z0-9_A-Z]+:[0-9]+>", s)
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