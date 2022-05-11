import discord
import json
from discord.ext import commands
from discord import RawReactionActionEvent


class ReactionRole(commands.Cog):

    def __init__(self, client):
        self.client = client # sets the client variable so we can use it in cogs'
        self._last_member = None

    #---互動表情新增身分組---
    @commands.Cog.listener()
    async def on_raw_reaction_add(self , payload: RawReactionActionEvent):
        
        if str(payload.message_id) not in data:
            print(str(payload.message_id))
            return
        
        if str(payload.emoji) in data[str(payload.message_id)]:
            role = discord.utils.get(payload.member.guild.roles, name=data[str(payload.message_id)][str(payload.emoji)])
            await payload.member.add_roles(role)
            
    #---互動表情移除身分組---
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self , payload: RawReactionActionEvent):
        
        if str(payload.message_id) not in data:
            return

        if str(payload.emoji) in data[str(payload.message_id)]:
            guild = self.client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=data[str(payload.message_id)][str(payload.emoji)])
            await guild.get_member(payload.user_id).remove_roles(role)

    #---綁定互動表情身分組---
    @commands.command()
    @commands.has_role(848555690292150273)
    async def reaction_role(self, ctx, message_id:int ,emoji:str, roles:discord.Role):

        with open('./data/reaction_role.json','r+') as file:
            data = json.load(file)

            if message_id not in data:
                data.update({str(message_id):{}})
                
            data[str(message_id)].update({str(emoji):str(roles)})
            file.seek(0)
            json.dump(data, file, indent = 4)
        
        await ctx.message.delete()

    #---機器人按表情---
    @commands.command()
    async def add_emoji(self,ctx,message_id:int , emoji:str):
        message =  await ctx.fetch_message(message_id)
        await message.add_reaction(emoji)
        await ctx.message.delete()

    #---報錯區域---
    @reaction_role.error
    async def roles_error(self, ctx, error):
        if ("is required to run this command." in str(error)):
            await ctx.send("you dont have permission")
        else:
            await ctx.send("try to use &reaction_role message_id emoji roles")

    @on_raw_reaction_add.error
    async def on_raw_reaction_add_error(self, ctx, error):
        await ctx.send("please check your bot permission is bigger than the role you want to get")

    @on_raw_reaction_remove.error
    async def on_raw_reaction_remove_error(self, ctx, error):
        await ctx.send("please check your bot permission is bigger than the role you want to get")


def setup(client):
    global data
    with open('./data/reaction_role.json', 'r') as f:
        data = json.load(f)
    client.add_cog(ReactionRole(client))
