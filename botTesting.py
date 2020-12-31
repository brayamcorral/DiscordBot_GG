#                           bot.py
#                Python with Discord api
# Code written by Brayam Corral, Samuel Min, Edgar Ubaldo. 

#                         RULES
# Discord bot lets you play gungame, variant of rocks, papers, scissors.
# Play against the computer: Can shoot, block, or reload.
# Blocking  -- Negates a shooting action from the computer.
# Reloading -- Increases number of bullets owned (up to a maximum of 5). 
# Shooting  -- Must have a bullet. If the oponent is reloading, you win. 
#              If both players shoot, nothing happens, other than losing a bullet.


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
playerTurn = False
correctInput = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global cpu_bullets, p1_bullets, cpu_won, p1_won, p1_action, cpu_action, moveOutcome, move, gunGame, playerTurn, correctInput

    if message.author == client.user:
        return

    if message.content==('$hello'):
        await message.channel.send('```Hello World!```')

    # Game starts with the keyWord: $play
    if message.content==('$play'):
        if(gunGame): 
            await message.channel.send('```Game has already started```')
        else:
            await message.channel.send('```Starting game...```')
            cpu_bullets = 1
            p1_bullets = 1
            cpu_won = False
            p1_won = False
            p1_action = 0
            cpu_action = 0
            moveOutcome = [ [0,0,0], [0,0,-1] ,[0, 1, 0] ]
            move = 0
            gunGame = True
            correctInput = True
            playerTurn = False
            
    if message.content==('$rules'):
        rules_message =  '```Play against the computer: Can shoot, block, or reload. \n' \
                        'Blocking  -- Negates a shooting action from the computer. \n' \
                        'Reloading -- Increases number of bullets owned (up to a maximum of 5). \n' \
                        'Shooting  -- Must have a bullet. If the oponent is reloading, you win. \n' \
                        '             If both players shoot, nothing happens, other than losing a bullet. \n```' \

        await message.channel.send(rules_message)
        return 

    if message.content==('$help'):
        help_message =  '```$rules -- Shows rules of GunGame \n' \
                        '$play -- Starts Game \n' \
                        '$end -- Ends Game' \

        await message.channel.send(help_message)
        return 

    if message.content==('$end'):
        if(gunGame):
            await message.channel.send('```Ending game...```')
            gunGame = False
            return
        else:
             await message.channel.send('```No game in progress```')
             return
    
        
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

    if(gunGame):
        # Gets the users action
        if((not p1_won) and (not cpu_won)):
            if message.content==('$0'):
                correctInput = True
                p1_action = 0
                playerTurn = True
                cpuAction()
            if message.content==('$1'):
                correctInput = True
                if (p1_bullets>0):
                    p1_action = 1
                    p1_bullets -= 1
                    playerTurn = True
                    cpuAction()
                else:
                    await message.channel.send("```No more bullets. Try Again.```")
                    return
            if message.content==('$2'):
                correctInput = True
                p1_action = 2
                p1_bullets += 1
                playerTurn = True
                cpuAction()

    if(not correctInput):
        await message.channel.send("```Wrong Input```")
        return

    # Prints out each player's bullets and determines if a player has shot one another (won) yet.
    if (not p1_won and not cpu_won):
        disc_message = ""
        
        if cpu_bullets > 5:
            cpu_bullets = 5
        if p1_bullets > 5:
            p1_bullets = 5

        disc_message += "```     P1 Bullets     CPU Bullets"+"\n"

        disc_message += "     "
        for n in range(p1_bullets):
            disc_message += "\u25AE"
        for n in range(5 - p1_bullets):
            disc_message += "\u25AF"

        disc_message += "      "

        for n in range(cpu_bullets):
            disc_message += "\u25AE"
        for n in range(5 - cpu_bullets):
            disc_message += "\u25AF"

        disc_message += "    "

        disc_message += "\n\n"

        # choices =    Block,          Shoot,        Reload
        choices = ['\U0001f6e1\uFE0F', '\U0001F3F9', '\U0001F504']

        if(playerTurn):
            disc_message += "       P1: " + choices[p1_action] + "        "  + "CPU: " + choices[cpu_action] + "\n\n"
            if moveOutcome[cpu_action][p1_action] == 1:
                p1_won = True
            if moveOutcome[cpu_action][p1_action] == -1:
                cpu_won = True  
            playerTurn = False
        disc_message += "Choose Action: \U0001f6e1\uFE0F[$0] \U0001F3F9[$1] \U0001F504[$2] " + "\n"
        await message.channel.send(disc_message + "```")
        correctInput = False

    # Prints which player won
    if(p1_won):
        await message.channel.send("```YOU WON```")
        gunGame = False
        playerTurn = True
    if(cpu_won):
        await message.channel.send("```YOU LOSE```")
        gunGame = False
        playerTurn = True
    
client.run(BOT_TOKEN)