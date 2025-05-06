from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands
import discord
import typing

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

class SuggestionCommand(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command()
    @has_permissions(administrator=True)
    @app_commands.describe(id='ID of the suggestion',option='Change the status of a suggestion',reason='The reason for this change of status')
    async def suggestion(self, interaction: discord.Interaction, id: str, option: typing.Literal['approve','table','update'],reason: str):
        try:
            #Look for the suggestion ID
            found = False
            async for message in interaction.channel.history():
                for checkembed in message.embeds:
                    if f"{id}" in f"{checkembed.title}":
                        found = True
                        newembed = checkembed.copy()
                        if(option == 'approve'):
                            newembed.color = 0x00FF00
                            newembed.set_author(name="Approved")
                            newembed.add_field(name="",value=f"Approved by <@{interaction.user.id}> \n{reason}", inline=False)

                        elif(option == 'table'):
                            newembed.color = 0x808080
                            newembed.set_author(name="Tabled")
                            newembed.add_field(name="",value=f"Tabled by <@{interaction.user.id}> \n{reason}", inline=False)

                        elif(option == 'update'):
                            newembed.set_author(name="")
                            newembed.add_field(name="",value=f"Updated by <@{interaction.user.id}> - voting has been reset! \n{reason}",inline=False)
                            await message.clear_reactions()
                            await message.add_reaction('⬆️')
                            await message.add_reaction('⬇️')

                        await message.edit(embed=newembed)

            await interaction.response.send_message(content="Done!",delete_after=0,ephemeral=True)

            #If the suggestion cannot be found
            if found == False:
                await interaction.channel.send(content=f"Suggestion #{id} could not be found!",delete_after=15)

        except Exception as e:
            print(str(e))
            await interaction.response.send_message(content='Error! Please check the console for more information.' ,ephemeral=True)