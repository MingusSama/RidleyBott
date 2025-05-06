import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

import discord.ui as ui  #for UI elements

from helpers.bothelpers import BotHelpers #My own helpers
import json #Needed to access the config
import datetime #Needed for the embed creation

class CreateSuggestionModal(ui.Modal, title='Suggestion'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.type = type

    preview = ui.TextInput(label="Title",style=discord.TextStyle.short,required=True,max_length=60)
    description = ui.TextInput(label="Link",style=discord.TextStyle.paragraph,required=True)
    async def on_submit(self,interaction:discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True,thinking=False)

            #Pull the current suggestion count, increment by 1.
            suggestion_id = BotHelpers.channel_increment(interaction.channel.id)
            suggestion_log_channel = await self.bot.fetch_channel(f"{interaction.channel_id}")
            
            #Creation of the suggestion embed, and sending the message
            embed = discord.Embed(title=f"Suggestion #{suggestion_id}",
                colour=0x00b0f4,
                description=f'**{self.preview}**\n{self.description}',
                timestamp=datetime.datetime.now())
            embed.set_footer(text=f"{interaction.user.display_name}",
                icon_url=f"{interaction.user.avatar}")
            
            #Sends message in staff channel, creates a thread with suggestion ID
            message = await suggestion_log_channel.send(embed=embed)            
            await message.create_thread(name=f"Discussion #{suggestion_id}")
            await message.add_reaction('⬆️')
            await message.add_reaction('⬇️')
            
            #Resends the bumper at the bottom of the chain
            await BotHelpers.purge_bumpers(self,interaction)
            from suggestion import suggestion_bumper_view
            view = suggestion_bumper_view.SuggestionButtonView(self.bot)
            message = await suggestion_log_channel.send(view=view, silent=True)
            
        except Exception as e:
            print(e)