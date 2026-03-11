file = open("Config.txt","r")
TOKEN = str(file.read())
file.close()
#The Token


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


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync() #(guild=discord.Object(id="1043885670629900288")) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@client.event
async def on_message(message):
    if not message.guild:
        if (message.author.bot):
            return

@tree.command(name = 'register', description='Register your character') #guild specific slash command
@app_commands.describe(char_name = "Your character name", avatar_url = "Your character avatar url")
async def register(interaction: discord.Interaction, char_name: str, avatar_url: str):
    try:
        Id = str(interaction.user.id)
        sql = "REPLACE INTO userdata (user_id, char_name, char_pic) VALUES (%s, %s, %s)"
        val = (Id, char_name, avatar_url)
        cursor.execute(sql, val)
        mydb.commit()
        await interaction.response.send_message(f"Registration successful!", ephemeral = True)
    except:
        await interaction.response.send_message(f"Registration failed.", ephemeral = True)


@tree.command(name = 'speak', description='Speak!') #guild specific slash command
#@app_commands.checks.cooldown(1, 180.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.describe(whattosay = "What do you want to say?")
async def slash2(interaction: discord.Interaction, whattosay: str):
    #getting user details

    await interaction.response.send_message(content="Sending...", ephemeral = True, delete_after = 0)
    Id = str(interaction.user.id)
    try:
    #if True == True:

        sql = "SELECT * FROM userdata WHERE user_id=(%s)"
        cursor.execute(sql,(Id,))
        SQLout = cursor.fetchone()
        #print(SQLout) 
        #message = str(await interaction.original_response())


        #webhook = await interaction.channel.create_webhook(name="Dawn")
        webhooks = await interaction.channel.webhooks()
        #print(webhooks)
        try:
            for webhook in webhooks:
                #contents = urlopen(avatar_url).read()
                #await webhook.edit(name=username,avatar=contents)

                await webhook.send(content=whattosay,username=SQLout[1],avatar_url=SQLout[2])
        except:
            do = "nothing"
        #username=str(interaction.user), avatar_url=str(interaction.user.display_avatar)
        # webhooks = await interaction.channel.webhooks()
        # for webhook in webhooks:
    except:
   # else:
        await interaction.response.send_message(f"DM me anything for how to register!", ephemeral = True) 

@tree.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)
        
@tree.command( name = 'help', description='Learn') #guild specific slash command
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"DM me anything for how to register!", ephemeral = True)

#@client.event
#async def on_ready():
#    await tree.sync(guild=discord.Object(id="1043885670629900288")) #guild specific: leave blank if global (global registration can take 1-24 hours)


    #sql = "SELECT char_name FROM userdata WHERE user_id=(%s)"
    #cursor.execute(sql,("123456789",))
    #myresult = cursor.fetchone()
    #print(myresult[0])
    #Working SQL code to get character name from database using user id. Uncomment and change the user id to test.


    #user = await client.fetch_user("301013678051033090")
    #await user.send("Bot is now online!")

client.run(TOKEN)
