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
    updatedlist=[] #this part reads the .csv file and removes the users where their endtimes are over
    with open("logs.csv",newline="") as f:
      reader=csv.reader(f)
      for row in reader: 
        try:
            if str(row[3])>str(datetime.now()):
                updatedlist.append(row)
        except:
            pass
      UpdateFile(updatedlist)

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


def UpdateFile(updatedlist): #used to update the new log.csv file everytime a endtime is reached
    with open("logs.csv","w",newline="") as f:
        Writer=csv.writer(f)
        Writer.writerow(['user', 'begin_time', 'duration', 'endtime'])
        Writer.writerows(updatedlist)
        print("File has been updated")


client.run(Info.TOKEN)
