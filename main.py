from config_handler import load_config

import sys
import discord

#Access config data============================
config = load_config()

#Get Credentials
secret = config["credentials"]["TOKENsecret"]

#Exception handling so that the discord bot wont start if theres no TOKEN
if secret == '' or secret == 'your_TOKEN_secret_here':
    print("No TOKEN secret detected please enter your token.")
    sys.exit(0)
#========================================================================

class Client(discord.Client):
    #Runs when the discord bot goes online
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
#Put your discord bot token here
client.run(secret)