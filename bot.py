# bot.py
import discord
import os 
import requests
import json 

BOT_TOKEN = ''
client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game('IDLE'))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

    if message.content.startswith('$test'):
        await message.channel.send('Working')

    if message.content.startswith('$speak'):
        quote = get_quote()
        await message.channel.send(quote)

client.run(BOT_TOKEN)

