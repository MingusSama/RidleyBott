import discord
import json
import datetime
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

class BotHelpers():
    def __init__(self, bot: "Bot"):
        self.bot = bot
        
    #####################
    #DISCORD HELPERS
    #####################

    #Parses through messages in the channel where the interaction occured, and deletes them if they are silent and sent by the bot
    async def purge_bumpers(self, interaction: discord.Interaction):
        async for message in interaction.channel.history(limit=25):
            if message.flags.silent == True:
                if message.author.id ==1259505092357390338 :
                    await message.delete()

    #Parses through messages in the channel specified, and deletes them if they are silent and sent by the bot
    async def purge_bumpers_ch(self, channel: discord.TextChannel):
        async for message in channel.history(limit=25):
            if message.flags.silent == True:
                if message.author.id == 1259505092357390338:
                    await message.delete()

    #####################
    #CONFIG HELPERS (config.json)
    #####################

    #Reads the config JSON
    def read_config():
        with open('config.json','r') as file:
            config = json.load(file)
        return config
    
    #Records the new channel information into config.json
    def channel_add(channel_id,option,channel_name):
        config = BotHelpers.read_config()
        #Record new channel information in JSON
        new_channel_info = {
                "id": f"{channel_id}",
                "type": f"{option}",
                "count": 0
                }
        config["channels"][f"{channel_name}"] = new_channel_info
        with open('config.json','w') as file:
            json.dump(config,file,indent=4)

    #Looks up the channel type based off given ID, returns the type or None if it DNE
    def channel_lookup(channel_id):
        config = BotHelpers.read_config()
        channel_type=None
        for channel in config["channels"]:
            if config["channels"][f"{channel}"]["id"] == f"{channel_id}":
                channel_type = config["channels"][f"{channel}"]["type"]
        return channel_type

    #Increments the current count of the channel, returns the old count + optional letter arg.
    def channel_increment(channel_id:int):
        config = BotHelpers.read_config()
        #Looks through the list for the channel, records letter and count
        for channel in config["channels"]:
            if config["channels"][f"{channel}"]["id"] == f"{channel_id}":
                    channel_count = int(config["channels"][f"{channel}"]["count"])
                    try:
                        channel_letter = config["channels"][f"{channel}"]["letter"]
                    except:
                        channel_letter = ""
                    config["channels"][f"{channel}"]["count"] = f"{channel_count + 1}"
        #Writes back to the config
        with open('config.json','w') as file:
            json.dump(config,file,indent=4)
        #Returns the letter + ID
        current_id = f"{channel_letter}{channel_count}"
        return current_id

    #####################
    #TICKET HELPERS (ticket.json)
    #####################

    #Creates a new ticket entry
    def create_ticket(thread_id:int,user_id:int,mcuser,subj,desc,ticket_id):
        with open('tickets.json','r') as ticketfile:
            ticketlog = json.load(ticketfile)
        #Log new ticket
        timestamp = datetime.datetime.now()
        epoch = round(timestamp.timestamp())
        new_ticket_info = {
                    "thread_id": f"{thread_id}",
                    "user_id": f"{user_id}",
                    "status": "New",
                    "mcuser": f"{mcuser}",
                    "subj": f"{subj}",
                    "desc": f"{desc}",
                    "epoch": f"{epoch}"
                    }
        ticketlog[f"{ticket_id}"] = new_ticket_info
        #Write to tickets json
        with open('tickets.json','w') as ticketfile:
            json.dump(ticketlog,ticketfile,indent=4)

    #Changes status of a ticket
    def update_ticket_status(thread_id,new_status):
        #Load ticket json
        with open('tickets.json','r') as ticketfile:
            ticketlog = json.load(ticketfile)
        #change status in the JSON
        for ticket in ticketlog:
            threadid = ticketlog[ticket]["thread_id"]
            if int(threadid) == thread_id:
                ticketlog[f"{ticket}"]["status"] = new_status
        #write to ticket
        with open('tickets.json','w') as ticketfile:
            json.dump(ticketlog,ticketfile,indent=4)