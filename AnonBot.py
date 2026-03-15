file = open("Config.txt","r")
TOKEN = str(file.read())
file.close()
#Config.txt contains the bot token, located on working machine.


import mysql.connector
import discord
from discord import app_commands
import json
import ast
import time
from urllib.request import urlopen
import base64


mydb = mysql.connector.connect(
  host="localhost",
  user="CustomSenderBot",
  password="",
  database="CustomSenderBotData"
)
cursor = mydb.cursor()
#Database details, located on working machine.


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync() #(guild=discord.Object(id="1043885670629900288")) #Testing ID
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

#@client.event
#async def on_message(message):
#    if not message.guild:
#        if (message.author.bot):
#            return

@tree.command(name = 'register', description='Register your character') #guild specific slash command
@app_commands.describe(char_name = "Your character name", avatar_url = "Your character avatar url")
async def register(interaction: discord.Interaction, char_name: str, avatar_url: str):
    try:
        Id = str(interaction.user.id)
        sql = "REPLACE INTO userdata (user_id, char_name, char_pic) VALUES (%s, %s, %s)"
        val = (Id, char_name, avatar_url)

        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        await interaction.response.send_message(f"Registration successful!", ephemeral = True)
    except:
        await interaction.response.send_message(f"Registration failed.", ephemeral = True)


@tree.command(name = 'speak', description='Speak!')
@app_commands.describe(whattosay = "What do you want to say?")
async def slash2(interaction: discord.Interaction, whattosay: str):
    #getting user details

    await interaction.response.send_message(content="Sending...", ephemeral = True, delete_after = 0)
    Id = str(interaction.user.id)
    try:

        sql = "SELECT * FROM userdata WHERE user_id=(%s)"

        cursor = mydb.cursor()
        cursor.execute(sql,(Id,))
        SQLout = cursor.fetchone()

        webhooks = await interaction.channel.webhooks()
        try:
            for webhook in webhooks:
                #whattosay="```ansi\n\u001b[0;31mThis is red text\u001b[0m\n\u001b[0;32mThis is green text\u001b[0m\n\u001b[1;34mThis is bold blue text\u001b[0m\n```"
                await webhook.send(content=whattosay,username=SQLout[1],avatar_url=SQLout[2])
        except:
            await interaction.response.send_message(f"Message failed, possible issue with registration details.", ephemeral = True) 

    except:
        await interaction.response.send_message(f"Register first.", ephemeral = True) 

@tree.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)

client.run(TOKEN)
