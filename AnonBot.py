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
            await tree.sync(guild = discord.Object(id="")) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@client.event
async def on_message(message):
    if not message.guild:
        if (message.author.bot):
            return

        Message = (message.content).split("#####")
        if Message[0] == "REGISTER":
            
            file = open("Faces.DAWN","r")
            Faces = ast.literal_eval(file.read())
            file.close()

            try:
                Id = str(message.author.id)
                New = True
                Count = 0
                for X in Faces:
                    if X[0] == Id:
                        X[1] = Message[1]
                        X[2] = Message[2]
                        
                        file = open("Faces.DAWN","w")
                        file.write(str(Faces))
                        file.close()
                        New = False

                    Count = Count + 1
                    if Count == (len(Faces)):
                        if New == True:
                            Faces.append([Id,Message[1],Message[2]])
                            file = open("Faces.DAWN","w")
                            file.write(str(Faces))
                            file.close()
                            New = False



                await message.channel.send('Registered!')

            except:
                await message.channel.send('Incorrect Format')
            
        else:
            await message.channel.send('Please register by typeing a message like this:')
            await message.channel.send('REGISTER#####NAME HERE#####IMAGE LINK HERE')
            await message.channel.send("Like this: REGISTER#####Charles Whitmee#####https://i.postimg.cc/pr5Qw0C2/Chill-Copy.png")
        

            

@tree.command(name = 'speak', description='Speak!') #guild specific slash command
#@app_commands.checks.cooldown(1, 180.0, key=lambda i: (i.guild_id, i.user.id))
@app_commands.describe(whattosay = "What do you want to say?")
async def slash2(interaction: discord.Interaction, whattosay: str):
    #getting user details
    file = open("Faces.DAWN","r")
    Faces = ast.literal_eval(file.read())
    file.close()

    await interaction.response.send_message(content="Sending...", ephemeral = True, delete_after = 0)
    Id = str(interaction.user.id)
    try:
    #if True == True:
        for X in Faces:
            if X[0] == Id:
                username = str(X[1])
                avatar_url = str(X[2])
                #message = str(await interaction.original_response())


                #webhook = await interaction.channel.create_webhook(name="Dawn")
                webhooks = await interaction.channel.webhooks()
                #print(webhooks)
                try:
                    for webhook in webhooks:
                        #contents = urlopen(avatar_url).read()
                        #await webhook.edit(name=username,avatar=contents)

                        await webhook.send(content=whattosay,username=username,avatar_url=avatar_url)
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
        
@tree.command( name = 'help', description='Learn"') #guild specific slash command
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"DM me anything for how to register!", ephemeral = True)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id="1043885670629900288")) #guild specific: leave blank if global (global registration can take 1-24 hours)


    sql = "SELECT name FROM userdata WHERE pid=?"
    cursor.execute(sql,"123456789")
    myresult = cursor.fetchone()
    print(myresult)
    
    #user = await client.fetch_user("301013678051033090")
    #await user.send("Bot is now online!")

client.run(TOKEN)
