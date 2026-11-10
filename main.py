from config_handler import load_config

import sys
import json
import random

from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands

SCRIPT_DIR = Path(__file__).resolve().parent

#============================
config = load_config()                                                                      #Access config data
secret = config["credentials"]["TOKENsecret"]                                               #Get Credentials
serverID = 896543399124033567                                                               #Sync slash commands to a specific server
with open(SCRIPT_DIR/"data.json", "r", encoding="utf-8") as file: data = json.load(file)    #Ingest the data.json file as a Python Dictionary
#========================================================================
#------------------------------------------------------------------------

#Declaring the Omikuji Function for the bot to use
def gacha_Omikuji():
    RNGpick = random.choice(list(data.keys()))
    entryKEY = data[RNGpick]

    Character = entryKEY["character"]
    Alignment = entryKEY["alignment"]
    Intro = entryKEY["intro"]
    FlavorText = entryKEY["flavortext"]
    ImagePath = SCRIPT_DIR/"images"/f"{RNGpick}.png"

    # print(RNGpick)
    # print(Character)
    # print(FlavorText)
    # print(ImagePath)

    return Character, Alignment , Intro , FlavorText , ImagePath

#=====================================================
#Class Function for the bot
class Client(commands.Bot):
    #Runs when the discord bot goes online
    async def on_ready(self):
        try:
            guild = discord.Object(id=serverID)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

        print(f'\nLogged on as {self.user}\n=======================================================')

    #Detects and knows from who the messages come from
    async def on_message(self, message):
        if message.author == self.user: return #Disallows the bot from replying to itself
        #if message.content == 'ping': await message.channel.send('pong')

#-----------------------------------------------------------------
#=================================================================

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=serverID) #allow Slash Command only for this Discord Server thats defined

#Declaration Slash Commands==========
@client.tree.command(name="omikuji",description="Pull your fortune slip for the incoming year", guild=GUILD_ID)
async def omikuji(interaction: discord.Interaction):
    chara, alignment, intro, text, img = gacha_Omikuji()

    await interaction.response.send_message(
        f'{interaction.user.mention}\n'
        f'Recieved {alignment} from {chara}, {intro}\n'
        f'{text}'
        f'\n{img}'
    )

client.run(secret) #Gets the discord bot token from config.yaml