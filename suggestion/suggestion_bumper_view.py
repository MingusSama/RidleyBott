import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

import discord.ui as ui  #for UI elements

class SuggestionButtonView(ui.View):
    def __init__(self, bot: "Bot"):
        super().__init__(timeout=None)
        self.bot = bot
	
    @ui.button(label="Suggest Movie",style=discord.ButtonStyle.primary,custom_id="createsuggestion")
    async def submit_suggestion_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:            
            from suggestion.suggestion_create_modal import CreateSuggestionModal
            await interaction.response.send_modal(CreateSuggestionModal(self.bot))
            
        except Exception as e:
            print(str(e))
            await interaction.response.send_message(content='Error! Please check the console for more information.' ,ephemeral=True)

    @ui.button(label="Help",style=discord.ButtonStyle.secondary,custom_id="helpsuggestion")
    async def add_note_suggestion_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:  
            help_embed = discord.Embed()
            help_embed.add_field(name="Suggestions Help",
                value="You can make any suggestions to improve the server here! Press the `Create Suggestion` button, and you'll be off to the races. Suggestions are first open to members of this server for comment, then are reviewed by the developer team for viability, and finally by the relevant team for implementation. Implementation timelines may vary, thank you for your patience and contribution!",
                inline=False)
            help_embed.set_footer(text="Message here - I self destruct in 30 seconds!")

            if interaction.user.guild_permissions.administrator == True:
                help_embed.add_field(name="Administrator Tools",
                    value="In order to change the status of a suggestion, use:\n`/suggestion <ID> <Action> <Reason/Comment>`\n> Update adds your comment, and resets vote reactions so they may be voted on again.",
                    inline=False)

            await interaction.response.send_message(embed=help_embed, ephemeral=True,delete_after=30)

        except Exception as e:
            print(str(e))
            await interaction.response.send_message(content='Error! Please check the console for more information.' ,ephemeral=True)