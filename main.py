import sys
import subprocess
import importlib.util

required_modules = {
    "yaml": "PyYAML",
    "discord": "discord.py"
}

for module, package in required_modules.items():
    if importlib.util.find_spec(module) is None:
        print(f"{package} is missing. Installing...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package
        ])
#==========================================================

import json
import random

from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands

from config_handler import load_config

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
    #RNGpick = "3"
    RNGpick = random.choice(list(data.keys()))
    entryKEY = data[RNGpick]

    Character = entryKEY["character"]
    Alignment = entryKEY["alignment"]
    Intro = entryKEY["intro"]
    FlavorText = entryKEY["flavortext"]
    ImagePath = SCRIPT_DIR/"images"/f"{RNGpick}.png"

    match Alignment:
        case "3": Alignment = "Great Blessing 「 大吉 」"
        case "2": Alignment = "Good Fortune 「 吉 」"
        case "1": Alignment = "Small Luck 「 小吉 」"
        case "0": Alignment = "No Alignment 「 無 」"
        case "-1": Alignment = "Future Blessing 「 末吉 」"
        case "-2": Alignment = "Small Curse 「 呪 」"
        case "-3": Alignment = "Great Curse 「 凶 」"
        case _: raise ValueError(f"Unknown alignment: {Alignment}")

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

#Omikuji Embed version Slash Commands==========
@client.tree.command(name="omikuji",description="Pull your fortune slip for the incoming year", guild=GUILD_ID)
async def omikuji(interaction: discord.Interaction):
    chara, alignment, intro, text, img = gacha_Omikuji()
    embed = discord.Embed(
        title=f"{alignment}",
        description=f"Your fortune has led you to {chara}!",
        color=discord.Color.gold()
    )
    embed.add_field(name=f"---",value=f"",inline=False)
    embed.add_field(name=f"",value=f"**{intro}**\n\n{text}",inline=False)
    file = discord.File(img)
    embed.set_image(url=f"attachment://{img.name}")
    await interaction.response.send_message(embed=embed,file=file)


# #Omikuji Slash Commands==========
# @client.tree.command(name="omikujitext",description="Pull your fortune slip for the incoming year", guild=GUILD_ID)
# async def omikuji(interaction: discord.Interaction):
#     chara, alignment, intro, text, img = gacha_Omikuji()

#     await interaction.response.send_message(
#         f'{interaction.user.mention}\n'
#         f'Recieved {alignment} from {chara}, {intro}\n'
#         f'{text}'
#         f'\n{img}'
#     )

client.run(secret) #Gets the discord bot token from config.yaml