from enum import Flag
import discord
import json
from discord.ext import commands
from discord import RawReactionActionEvent
import emoji
import re


class Vote(commands.Cog):

    def __init__(self, client):
        self.client = client # sets the client variable so we can use it in cogs'
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        global data , path
        path = './data/vote.json'
        data = load_json(path)

    @commands.command()
    async def vote(self, ctx, title , time , *arg):
            

        try:
            data
        except NameError:
            path = './data/vote.json'
            data = load_json(path)

        if len(arg)%2 != 0:
            await ctx.send("wrong format")
            await ctx.message.delete()
            return
        
        for i in range(int(len(arg)/2)):
            if(not (is_emoji(arg[i*2]) or is_discord_emoji(arg[i*2])) ):
                await ctx.send("wrong format")
                await ctx.message.delete()
                return

        message_id = ctx.message.reference.message_id


        message =  await ctx.fetch_message(message_id)

        if message_id not in data:
            data.update({str(message_id):{}})
            data = write_json(path,data)
        
        for i in range(int(len(arg)/2)):
            data[str(message_id)].update({arg[i*2]:arg[i*2+1]})
            data = write_json(path,data)
            await message.add_reaction(arg[i*2])
        
        await ctx.message.delete()


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