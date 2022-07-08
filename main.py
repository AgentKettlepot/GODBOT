import discord
import Info
import re
from datetime import datetime 
import csv
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
        now = datetime.now()
        end_time = now + time
        with open('logs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([message.author, now, time, end_time])
 
        await message.channel.send(f'{time[0]} minute timer set')


#add a function that is async def on_repeat (idk)
#keeps reading the .csv file, looks for anyone has messaged:
#if message.time is within the endtime column for message.author: send message
#remove elements where the end_time is already over
client.run(Info.TOKEN)
