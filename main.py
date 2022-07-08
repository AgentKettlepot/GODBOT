import discord
import Info
import re
from datetime import datetime, timedelta
import csv
import pandas as pd
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    ''' FIX THIS SECTION: SOMEHOW DELETE EVERY ROW IN .CSV FILE WHERE THE ENDTIME IS ALREADY OVER
    now = datetime.now() #this part removes rows where the endtime has already passed
    df = pd.read_csv('logs.csv')
    print(df)
    df = df[str(df.iloc[:,3]) > str(now)]
    df.to_csv('logs.csv', index=False)
    '''
    with open('logs.csv', 'r') as f: #this part reads the .csv file when someone sends a message
        reader = csv.reader(f)
        for line in reader:
            if len(line) != 0:
                if str(message.author) == line[0]:
                    await message.channel.send(f'{message.author} should NOT be on Discord!!!!')
                    break

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

#add a function that removes row once time_end is finished
client.run(Info.TOKEN)
