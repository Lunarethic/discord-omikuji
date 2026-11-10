from config_handler import load_config

import sys

import discord
from discord.ext import commands
from discord import app_commands

#============================
config = load_config() #Access config data
secret = config["credentials"]["TOKENsecret"] #Get Credentials
serverID = 896543399124033567 #Sync slash commands to a specific server
#========================================================================
#------------------------------------------------------------------------

#Declaring the Omikuji Function for the bot to use
def gacha_Omikuji():
    print('gacha attempt')

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

        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there! {message.author}')

#-----------------------------------------------------------------
#=================================================================
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=serverID) #allow Slash Command only for this Discord Server thats defined

#Declaration Slash Commands==========
@client.tree.command(name="omikuji",description="Pull your fortune slip for the incoming year", guild=GUILD_ID)
async def omikuji(interaction: discord.Interaction):
    gacha_Omikuji()
    print(f'omikuji command triggered by: {interaction.user}')
    print(f'rolled a 1')
    print(f'sending message to the user')

    await interaction.response.send_message(
        f'{interaction.user.mention}\n'
        f'To you who drew Lunar\\Sanco, Haha number!\n'
        f'Good luck in the coming year!'
    )

client.run(secret) #Gets the discord bot token from config.yaml