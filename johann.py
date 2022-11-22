# bot.py
#System modules
import os
from dotenv import load_dotenv

#3rdParty modules
import discord

#My modules
import pinger

load_dotenv()
load_dotenv('.key')

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#contains state representation 
class Johann:
    intents = discord.Intents.default()
    intents.messages = True
    intents.typing = False
    intents.presences = False
    client = discord.Client(intents=intents)
    pingerThread = {}
    channelList = []
    #async def alarm(value):

# BOT BEHAVION

johannBot = Johann()

@johannBot.client.event
async def on_ready():
    if len(johannBot.client.guilds) > 0:
        for guild in johannBot.client.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{johannBot.client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
        johannBot.pingerThread = pinger.Pinger(name = "Thread-{}".format(0))
        johannBot.pingerThread.start()

@johannBot.client.event
async def on_message(message):
    print('got message' + str(message.content))
    if message.channel not in johannBot.channelList:
        johannBot.channelList.append(message.channel)

    if message.content.startswith('$hello'):
        await message.channel.send('Halo!!')
        return  
        
    if '$ciao' in message.content:
        await message.channel.send('halo bambino!!')
        return

    if '$help' in message.content:
        await message.channel.send('Type @Johannt the alarm boot $ping to get ping information ')
        return

    if '$ping' in message.content:
        valuePairs = johannBot.pingerThread.getAverage()
        for value in valuePairs:
            await message.channel.send("Address: " + value.address +" has an average ping delay of: "+ str(value.averageDelay) + 'ms')
        return

    #testing method
    if '$submerge' in message.content:
        with open('alarm.gif', 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

johannBot.client.run(TOKEN)