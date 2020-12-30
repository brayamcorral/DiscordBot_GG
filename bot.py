#                           bot.py
#                Python with Discord api
# Code written by Brayam Corral, Samuel Min, Edgar Ubaldo. 

#                         RULES
# Discord bot lets you play gungame, variant of rocks, papers, scissors.
# Player plays against the computer and can shoot, block or reload.
# Blocking, negates a shooting action from the computer.
# Shooting, must have a bullet, shoots the oponent and wins if 
# the oponent is reloading. Reloading increase number of bullets owned.
# If both players shoot, nothing happens other than losing a bullet.

import random
import discord
import os 
import requests
import json 

BOT_TOKEN = ''
client = discord.Client()

# Global variables:
# shield : 0 | shoot : 1 | reload : 2
cpu_bullets = 1
p1_bullets = 1
cpu_won = False
p1_won = False
p1_action = 0
cpu_action = 0
moveOutcome = [ [0,0,0], [0,0,-1], [0, 1, 0] ]
move = 0
gunGame = False


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
    global cpu_bullets, p1_bullets, cpu_won, p1_won, p1_action, cpu_action, moveOutcome, move, gunGame

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

    if message.content.startswith('$speak'):
        quote = get_quote()
        await message.channel.send(quote)

    # Game starts with the keyWord: $play
    if message.content.startswith('$play'):
        if(gunGame): 
            await message.channel.send('Game has already started')
        else:
            await message.channel.send('Starting game...')
            await message.channel.send('Choose $0, $1, $2')
            cpu_bullets = 1
            p1_bullets = 1
            cpu_won = False
            p1_won = False
            p1_action = 0
            cpu_action = 0
            moveOutcome = [ [0,0,0], [0,0,-1] ,[0, 1, 0] ]
            move = 0
            gunGame = True

    # Game ends with keyWord: $end
    if message.content.startswith('$end'):
        if(gunGame):
            await message.channel.send('Ending game...')
            gunGame = False
        else:
             await message.channel.send('No game in progress')

    # CPU chooses action
    def cpuAction():
        global cpu_bullets, cpu_action
        if(cpu_bullets != 0):
            if(p1_bullets == 0):
                cpu_action = random.randint(1, 2)
            else:
                cpu_action = random.randint(0,2)
        elif (cpu_bullets == 0):
            if(p1_bullets == 0):
                cpu_action = 2
            else:
                cpu_action = random.choice([0, 2])
        else:
            cpu_action = 0
        if(cpu_action == 2): cpu_bullets += 1
        if(cpu_action == 1): cpu_bullets -= 1

   # Gets the users action
    if(gunGame and (not p1_won) and (not cpu_won)):
        if message.content.startswith('$0'):
            p1_action = 0
            cpuAction()
        if message.content.startswith('$1'):
            p1_action = 1
            p1_bullets -= 1
            cpuAction()
        if message.content.startswith('$2'):
            p1_action = 2
            p1_bullets += 1
            cpuAction()
        
    # Prints out each player's bullets and determines if a player has shot one another (won) yet.
    if (not p1_won and not cpu_won):
        choices = ['Shield', 'Shoot', 'Reload']
        await message.channel.send("Player Bullets = " + str(p1_bullets))
        await message.channel.send("CPU Bullets = " + str(cpu_bullets))
        await message.channel.send("CPU action = " + choices[cpu_action])
        if moveOutcome[cpu_action][p1_action] == 1:
            p1_won = True
        if moveOutcome[cpu_action][p1_action] == -1:
            cpu_won = True  
        if moveOutcome[cpu_action][p1_action] == 0:
            await message.channel.send("Choose Action: Shield[0] Shoot[1] Reload[2] " + "\n")

    # Prints which player won
    if(p1_won):
        await message.channel.send("YOU WON")
        gunGame = False
    if(cpu_won):
        await message.channel.send("YOU LOSE")
        gunGame = False
        
client.run(BOT_TOKEN)
