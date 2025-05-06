import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

from discord import app_commands    #for cogs
from discord.ext import commands    #for cogs
from discord.ext.commands import has_permissions #to restrict cmd usage to a permission

from helpers.bothelpers import BotHelpers #My own helpers
import json #Needed to access the config

class SetupCommand(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command()
    @has_permissions(administrator=True)
    @app_commands.describe(option='Designate channel for')
    async def setup(self,  interaction: discord.Interaction, option: typing.Literal['suggestion','control','support']):
        await interaction.response.defer(thinking=False)
        await interaction.channel.typing()

        channel_type = BotHelpers.channel_lookup(interaction.channel_id)

        #Check to see if the channel is already set up
        if channel_type != None:
            await interaction.channel.send(
                content=f"This channel is already designated as a {channel_type} channel.",
                delete_after=5)  
        else:
            #Creates a new entry based off options selected
            BotHelpers.channel_add(channel_id=interaction.channel_id,channel_name=interaction.channel.name,option=option)

        #Run the bumper for the channel depending on the type
        match f"{option}":
            case "suggestion":
                #Resends the bumper, deletes other silent messages
                await BotHelpers.purge_bumpers(self,interaction)
                from suggestion import suggestion_bumper_view
                suggestion_view = suggestion_bumper_view.SuggestionButtonView(self.bot)
                suggestion_message = await interaction.channel.send(view=suggestion_view, silent=True) 

        #Deletes the thinking defer symbol
        await interaction.delete_original_response()

