import discord
import Info
import re
from datetime import datetime, timedelta
import csv
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    users_on_time = []
    with open('logs.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            users_on_time.append(line[0])
    if message.author in users_on_time: #if the user is still in their restricted time
        await message.channel.send(f'{message.author} should NOT be on Discord!!!!')


    if message.content.startswith('$hello'):
        await message.channel.send('Hello!'+ str(message.author))
    
    if message.content.startswith('/setdailymax'):
        time = re.findall('[0-9]+', message.content)
        now = datetime.now()
        end_time = now + + timedelta(minutes = int(time[0]))  
        with open('logs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([message.author, now, time, end_time])
 
        await message.channel.send(f'{time[0]} minute timer set')


#add a function that is async def on_repeat (idk)
#keeps reading the .csv file, looks for anyone has messaged:
#if message.time is within the endtime column for message.author: send message
#remove elements where the end_time is already over
client.run(Info.TOKEN)
