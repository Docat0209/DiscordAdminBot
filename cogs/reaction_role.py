import discord
import json
from discord.ext import commands
from discord import RawReactionActionEvent
import emoji
import re


path = ""
data = None

class ReactionRole(commands.Cog):
    
    def __init__(self, client):
        self.client = client # sets the client variable so we can use it in cogs'
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        global data , path

        path = './data/reaction_role.json'
        data = load_json(path)
        print("recation_role online")

    #---互動表情新增身分組---
    @commands.Cog.listener()
    async def on_raw_reaction_add(self , payload: RawReactionActionEvent):
        global data , path

        if str(payload.message_id) not in data:
            return
        
        if str(payload.emoji) in data[str(payload.message_id)]:
            role = discord.utils.get(payload.member.guild.roles, name=data[str(payload.message_id)][str(payload.emoji)])
            await payload.member.add_roles(role)
            
    #---互動表情移除身分組---
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self , payload: RawReactionActionEvent):
        global data , path

        if str(payload.message_id) not in data:
            return

        if str(payload.emoji) in data[str(payload.message_id)]:
            guild = self.client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=data[str(payload.message_id)][str(payload.emoji)])
            await guild.get_member(payload.user_id).remove_roles(role)

    #---綁定互動表情身分組---
    @commands.command()
    @commands.has_role(848555690292150273)
    async def reaction_role(self, ctx,*arg):
        global data , path

        if ctx.message.reference is None :
            await ctx.send("you need to reply the message you want to add reaction_role")
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

            if(not is_discord_role(arg[i*2+1])):
                await ctx.send("wrong format")
                await ctx.message.delete()
                return

        message_id = ctx.message.reference.message_id


        message =  await ctx.fetch_message(message_id)

        data = load_json(path)

        if str(message_id) not in data:
            data.update({str(message_id):{}})
            data = write_json(path,data)
        
        for i in range(int(len(arg)/2)):
            role = discord.utils.get(ctx.guild.roles, id=int(arg[i*2+1][3:-1]))
            data[str(message_id)].update({arg[i*2]:str(role)})
            data = write_json(path,data)
            await message.add_reaction(arg[i*2])
        
        await ctx.message.delete()

    #---報錯區域---
    @reaction_role.error
    async def roles_error(self, ctx, error):
        if ("is required to run this command." in str(error)):
            await ctx.send("you dont have permission")
        else:
            await ctx.send(error)



async def setup(client):
    await client.add_cog(ReactionRole(client))

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