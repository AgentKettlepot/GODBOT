import discord
import Info
import re
from datetime import datetime, timedelta
import csv
from discord.ext import commands
import pandas as pd
import json 
import random
bot = commands.Bot(".")
commands = ['/cancel', '/onfocus', '/inspire', '/setdailymax', '!help']
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!help'):
        result = """Hi! I am the Get Off Discord Bot (GODBOT)! My purpose is to make sure that you
        stay focused. Here are my functions:
        1) /setdailymax <int>: sets a set minute timer
        2) /cancel: cancel the user's "focus mode\"
        3) /onfocus: lists the users currently in focus mode
        4) /inspire: gives a random inspiration/humorous quote
        Please use me to stay focused! Keep working hard!"""
        await message.channel.send(result)
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

    if message.content.startswith('/onfocus'):# displays the users currently on focus mode
        with open('logs.csv', 'r') as f:
            count=0
            reader = csv.reader(f)
            for line in csv.reader(f):
                    print(count)
                    if count>0:
                        await message.channel.send(line[0])
                    count+=1
            if len(list(reader))==0:
                await message.channel.send("None!")
                
    if message.content.startswith('/inspire'): #this part returns an inspirational quote to the user
        with open("unique_quotes.json") as JSONobject:
            pre_data = JSONobject.read()
            data = json.loads(pre_data)
            random_num= random.randint(1, len(data["data"])) - 1
            if "quote" in data["data"][random_num]:
                quote = data["data"][random_num]["quote"]
                author = data["data"][random_num]["author"]
                full_quote = quote + "-" + author
                await message.channel.send(full_quote)

    if message.content not in commands:
        with open('logs.csv', newline="") as f: #this part reads the .csv file when someone sends a message
            reader = csv.reader(f)
            total = list(reader)
            count=0
            for line in total:
                if len(line) != 0:
                    if str(message.author) == line[0]:
                        total[count] = [line[0], line[1], line[2], line[3], int(line[4])+1]
                        await message.channel.send(f'{message.author} should NOT be on Discord!!!!')
                        if int(line[4]) ==5:
                            await message.channel.send(f'{message.author}, this is your 5th warning! The next text will result in bullying!')
                        if int(line[4]) >=6:
                            mean_phrases = ['stinky', 'stupid']
                            index = random.random() * len(mean_phrases)
                            #find API or smth later instead of hard coding some bad words
                            await message.channel.send(f'{message.author.mention}, you are {mean_phrases[int(index)]}!!')
                            await message.author.edit(mute = True)

                count+=1
            UpdateFile(total)

    if message.content.startswith('/setdailymax'):
        time = re.findall('[0-9]+', message.content)
        now = datetime.now()
        end_time = now + + timedelta(minutes = int(time[0]))  
        with open('logs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([message.author, now, time[0], end_time,0])
 
        await message.channel.send(f'{time[0]} minute timer set')


def UpdateFile(updatedlist): #used to update the new log.csv file everytime a endtime is reached
    with open("logs.csv","w",newline="") as f:
        Writer=csv.writer(f)
        Writer.writerows(updatedlist)

bot.run(Info.TOKEN)
