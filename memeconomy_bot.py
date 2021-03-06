"""
memeconomy is a discord bot that tracks reactions across a discord challen.
"""
import discord
import os
import json
import time

bot_testing_channel_id = 584125656150048769
memeconomy_currency = ':xzibit:'     # custom emoji
memeconomy_emoji_id = '686709720090017821' # emoji id
memeconomy_emoji_str = '<' + memeconomy_currency + memeconomy_emoji_id + '>'
bank_file = 'bank.txt'

# load bank
if os.path.exists(bank_file):
    with open(bank_file) as json_file:
        bank = json.load(json_file)
        last_update_date = bank['timestamp']
        bank = bank['bank']
else:
    last_update_date = 0
    bank = {}


client = discord.Client()

# reference for fetching channel history: https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.history
# TODO: setup restore functionality based on 'last_update_date' that iterates through channels and populates missed currency to the bank, this should ignore bot channels
# TODO: incorporate bank for top memes
# TODO: add sort by options (sent / received) to leader
# TODO: add nth reaction celebration --- i.e., post a celebration when someone's bank hit's 100
# TODO: hidden emoji response -- listens for middle finger and flips person off back

# listen to all messages and listen to all reactions
# keep track of top memes

def top_meme (args = None):

    # channel = client.get_channel(meme_machine_channel_id)
    # messages = await ctx.channel.history(limit=200).flatten()
    return "[PLACEHOLDER]: top-meme command received"


def leader (args = None):
    """
    Creates a leaderboard from bank and converts it to a string
    """
    output_str = "Bank of " + memeconomy_emoji_str + " account balances \n" + "```"
    bank_sorted = sorted(bank.items(), key = lambda x: x[1]['received'], reverse=True)

    output_str += 'user'.ljust(16) + 'recd'.rjust(5) + 'sent'.rjust(5) + '\n'

    for user in bank_sorted:
        row = user[0].ljust(16) + str(user[1]['received']).rjust(5) + str(user[1]['sent']).rjust(5) + '\n'
        output_str += row
    
    output_str += "```"

    return output_str


# function dispatcher
dispatcher = {'top-meme': top_meme, 'leader': leader}


# Interprets the command received 
def memeconomy_command_processor(content):
    command_args = content.split(" ")
    
    if len(command_args) == 1:
        return "[PLACEHOLDER] No args, insert help menu here"

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
        reply_message = memeconomy_command_processor(message.content)

        await message.channel.send(reply_message)


# Reaction Object: https://discordpy.readthedocs.io/en/latest/api.html#discord.Reaction 
# User Object: https://discordpy.readthedocs.io/en/latest/api.html#discord.User
# channel = client.get_channel(bot_testing_channel_id)
# await channel.send("`" + str(payload.emoji) + "`")


async def update_bank(payload):
    """
    Updates the memecurrency bank
    """
    # Get the event type
    event_reference = {'REACTION_ADD': 1, 'REACTION_REMOVE': -1}
    transaction = event_reference[payload.event_type]

    # Get the username of person who reacted
    reactor = await client.fetch_user(payload.user_id)
    reactor_name = reactor.name # gets the display name

    # Get the username of the author
    channel = client.get_channel(payload.channel_id)
    partial_message = channel.get_partial_message(payload.message_id)
    message = await partial_message.fetch()
    author_name = message.author.name

    # Return if reactor and author are the same
    if reactor_name == author_name: 
        return
    
    # update the bank for the reactor
    if reactor_name not in bank.keys():
        bank[reactor_name] = {'received': 0, 'sent': 0}
    bank[reactor_name]['sent'] += transaction

    # update the bank for the author
    if author_name not in bank.keys():
        bank[author_name] = {'received': 0, 'sent': 0}
    bank[author_name]['received'] += transaction
    
    with open(bank_file, 'w') as outfile:
        json.dump({'timestamp' : time.time(), 'bank' : bank}, outfile)
    
    return


@client.event
async def on_raw_reaction_add(payload):
    """
    Add Reaction event listener
    This will take the payload

    message_id will be used to attribute the reaction to the original poster
    """
    if memeconomy_currency in str(payload.emoji):
        await update_bank(payload)
    return


@client.event
async def on_raw_reaction_remove(payload):
    """
    Remove Reaction event listener
    """
    if memeconomy_currency in str(payload.emoji):
        await update_bank(payload)
    return



client.run(os.getenv('DISCORD_TOKEN'))

