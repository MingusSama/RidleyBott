from discord.ext import commands
import discord
from datetime import datetime, timedelta
from discord.utils import utcnow
#/import cogs here
from helpers.setup import SetupCommand
from suggestion.suggestion import SuggestionCommand
#/import views here
from suggestion.suggestion_bumper_view import SuggestionButtonView

class Bot(commands.Bot):
    def __init__(self, **options):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True  # Important: We need member intents for checking join dates
        super().__init__(intents=intents, command_prefix='/')
   
    async def setup_hook(self):
        #/add views here
        self.add_view(SuggestionButtonView(self))
        
    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        #/add commands here
        await self.add_cog(SetupCommand(self))
        await self.add_cog(SuggestionCommand(self))
        synced = await self.tree.sync()
        print("{} commands synced".format(len(synced)))
    
    async def on_member_join(self, member):
        # Minimum account age requirement (7 days)
        minimum_age = utcnow() - timedelta(days=7)
        
        # Check if account is newer than minimum required age
        if member.created_at > minimum_age:
            # Account is too new (less than 7 days old)
            try:
                # Format dates for messages
                created_date = member.created_at.strftime("%Y-%m-%d UTC")
                
                # Try to send a DM to the user
                await member.send(
                    f"You have been removed from the server because your account is less than 7 days old. "
                    f"Your account was created on {created_date}. "
                    f"Please try joining again after your account is at least 7 days old."
                )
            except discord.Forbidden:
                # If DM can't be sent, just log it
                print(f"Could not send DM to {member.name}#{member.discriminator}")
            
            # Kick the user
            reason = f"Account age verification: Account created on {created_date}, less than 7 days ago."
            await member.kick(reason=reason)
            
            # Log the action
            print(f"Kicked user {member.name}#{member.discriminator} (ID: {member.id}) for having an account younger than 7 days.")
