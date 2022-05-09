import discord
import json
from discord.ext import commands
from discord import RawReactionActionEvent

class AddRole(commands.Cog):
    def __init__(self, client):
        self.client = client # sets the client variable so we can use it in cogs'

    with open('./data/add_role.json', 'r') as f:
        data = json.load(f)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self , payload: RawReactionActionEvent):
        MsgID = 973068106211655690
        if payload.message_id != MsgID:
            return
        if str(payload.emoji) == "<:ticket:973088738567655465>":
            role = discord.utils.get(payload.member.guild.roles, name="test")
            await payload.member.add_roles(role)
    

def setup(client):
    client.add_cog(AddRole(client))


