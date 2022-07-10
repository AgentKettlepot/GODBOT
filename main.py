import discord
import Info
import re
from datetime import datetime, timedelta
import csv
from discord.ext import commands

bot = commands.Bot(".")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    updatedlist=[] #this part reads the .csv file and removes the users where their endtimes are over
    with open("logs.csv",newline="") as f:
      reader=csv.reader(f)
      for row in reader: 
        try:
            if str(row[3])>str(datetime.now()):
                updatedlist.append(row)
            else:
                await message.channel.send(f'@{row[0]} has finished their focus session!')
        except:
            pass
      UpdateFile(updatedlist)

    if message.content.startswith('/cancel'):#this part cancels the user's focus mode
        with open('logs.csv', 'r') as f:
            reader = csv.reader(f)
            current_list = []
            for line in reader:
                current_list.append(line)
            if str(message.author) not in str([i[0] for i in current_list]): #if the user who uses /cancel is not in focus mode
                await message.channel.send('Currently not in focus mode')
            else:
                updatedlist = [i for i in current_list if str(i[0]) != str(message.author)]
                UpdateFile(updatedlist)
                await message.channel.send(f'{message.author} has been removed from focus mode!')



    with open('logs.csv', 'r') as f: #this part reads the .csv file when someone sends a message
        reader = csv.reader(f)
        for line in reader:
            if len(line) != 0:
                if str(message.author) == line[0]:
                    await message.channel.send(f'{message.author} should NOT be on Discord!!!!')
                    break


    if message.content.startswith('/setdailymax'):
        time = re.findall('[0-9]+', message.content)
        now = datetime.now()
        end_time = now + + timedelta(minutes = int(time[0]))  
        with open('logs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([message.author, now, time[0], end_time])
 
        await message.channel.send(f'{time[0]} minute timer set')






    if message.content.startswith('/onfocus'):# displays the users currently on focus mode
        with open('logs.csv', 'r') as f:
            reader = csv.reader(f)
            
            for line in reader:
                await message.channel.send(line)

def UpdateFile(updatedlist): #used to update the new log.csv file everytime a endtime is reached
    with open("logs.csv","w",newline="") as f:
        Writer=csv.writer(f)
        Writer.writerows(updatedlist)


bot.run(Info.TOKEN)
