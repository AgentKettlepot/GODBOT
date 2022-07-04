import discord


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('I'):
        await message.channel.send('Hello!')

client.run('OTkzNTYxNTkxMTI5ODU0MDky.GP1AYq.7GZ0Ax7lGudFxwPy3QFldYifC9FIXEDOImuwB0')
