import discord
import n_bot_calculator_core

#This file handles direct bot-discord user interactions. No background calculations or anything, though. Mostly reactive functions.


discordClient = discord.Client()

@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
#listens to sent messages for recognizable commands (expected to be at the start of a message)
async def on_message(message):
    requestGuild = message.guild
    requestGuildTxtChannels = requestGuild.text_channels
    #Interactive only. Might kill this later.
    if message.content.startswith('N_greet'):
        await message.channel.send('Hello!')

    #Output a help list for commands, explain usage syntax, etc.
    elif message.content.startswith('N_help'):
        await message.channel.send('TODO: Put a helpful list of commands here.')

    #Meat of the program. Acknowledges command - has background find them - then outputs.
    elif message.content.startswith('N_count'):
        await message.channel.send('Acknowledging order to count N-words for mentioned users.')
        N_countList = message.mentions
        #Pass the list of channels, and list of names to the message history parser.
        await message.channel.send('Now calculating NWord Counts (this could seriously take a while...)')
        N_countResults = await n_bot_calculator_core.message_search(requestGuildTxtChannels, N_countList)
        await message.channel.send('DEBUG: List of members')
        for N_countListMember in N_countList:
            await message.channel.send(N_countListMember.name + ' ID: ' + str(N_countListMember.id) + ' (number here)')
        await message.channel.send('DEBUG: Channels searched')
        for text_channel in requestGuildTxtChannels:
            await message.channel.send(text_channel.name)
        await message.channel.send('List of nwordCounts coming up...')
        for N_countListMember in N_countList:
            memberIDString = N_countListMember.name + '#' + str(N_countListMember.discriminator)
            await message.channel.send(memberIDString + ' NWord Count = ' + str(N_countResults[memberIDString]))

discordClient.run('ODc1Nzg0MTkwMTgyOTczNTQx.YRajlg.sklbdMAfFFcQdSSSxl3saLuJkU8')



# So far, the way this seems to work is by having an event loop somewhere in client,
# which constantly listens for events, and invokes callback functions pertaining to the event when one is registered.
# (in the background).

# The await key calls asynchronous functions (i.e. everything in discord.py).
# When python encounters an 'await' call, within a function, it will stop the parent function execution there,
# and do other work until it's ready to continue working on that function (once the await-called thing is done,
# probably). So we can do some parallel work in an easy way.
