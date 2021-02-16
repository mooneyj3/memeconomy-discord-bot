import discord
import os

client = discord.Client()

meme_machine_channel_id = 583874774674046976

def top_meme (args = None):
    return "[PLACEHOLDER]: top-meme command received"

def leader (args = None):
    return "[PLACEHOLDER]: leader command received"

dispatcher = {'top-meme': top_meme, 'leader': leader}


# Interprets the command received 
def command_processor(content):
    command_args = content.split(" ")
    
    if len(command_args) == 1:
        return "[PLACEHOLDER] No args"

    command = command_args[1]

    if command not in dispatcher.keys():
        return "[PLACEHOLDER] Invalid command option"
    
    return dispatcher[command]()


@client.event
async def on_ready(): 
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Handle mentions, this will trigger the bot to issue help
    if client.user in message.mentions:
        await message.channel.send('[PLACEHOLDER]: $memeconomy help')

    # Handle commands
    if message.content.startswith('$memeconomy'):
        reply_message = command_processor(message.content)

        await message.channel.send(reply_message)


client.run(os.getenv('DISCORD_TOKEN'))

