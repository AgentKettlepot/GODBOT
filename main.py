import discord
import Info
import re
from datetime import datetime 
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!'+ str(message.author))
    
    if message.content.startswith('/setdailymax'):
        time = re.findall('[0-9]+', message.content)
        print(time)
        now = datetime.now()
        await message.channel.send(f'{time} minute timer set')

client.run(Info.TOKEN)
