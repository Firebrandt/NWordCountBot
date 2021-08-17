import discord

import n_bot_calculator_core

#This file handles direct bot-discord user interactions. No background calculations or anything, though. Mostly reactive functions.


discordClient = discord.Client()

INT32_MAX = 2^32-1
discordClient.max_messages = INT32_MAX


@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
#listens to sent messages for recognizable commands (expected to be at the start of a message)
async def on_message(message):
    requestGuild = message.guild
    requestGuildTxtChannels = requestGuild.text_channels

    #The bot will ignore its own messages (for tripping commands).
    if message.author == discordClient.user:
        return

    #Output a help list for commands, explain usage syntax, etc.
    if message.content.startswith('N_help'):
        await message.channel.send('TODO: Put a helpful list of commands here.')

    #Meat of the program. Acknowledges command - has background find them - then outputs.
    elif message.content.startswith('N_count'):
        await message.channel.send('Acknowledging order to count N-words for mentioned users.')
        N_countList = message.mentions

        #Pass the list of channels, and list of names to the message history parser.
        await message.channel.send('Now calculating NWord Counts (this could seriously take a while...)')
        N_countResults = await n_bot_calculator_core.message_search(requestGuildTxtChannels, N_countList)

        await message.channel.send('List of nwordCounts coming up...')
        for N_countListMember in N_countList:
            memberIDString = N_countListMember.name + '#' + str(N_countListMember.discriminator)
            if N_countListMember.id != 186540780603703296:
                await message.channel.send(memberIDString + ' NWord Count = ' + str(N_countResults[memberIDString]))
            else:
                await message.channel.send('[[[!!!DEBUG: PROTECTED USER!!!]]] ' + memberIDString + ' NWord Count = ' + str(0))

@discordClient.event
async def on_message_edit(before, after):
    messageList = [before]
    requestMemberList = [before.author]
    nWordsinMessage = await n_bot_calculator_core.n_countCalculation(messageList, requestMemberList)
    if before.content != after.content and nWordsinMessage != 0:
        memberIDString = before.author.name + '#' + str(before.author.discriminator)
        await before.channel.send('Detected edit of message with the N-Word in it in this channel. By ' + memberIDString + '\n' + 'Original message contents: \"' + before.content + '\"')


@discordClient.event
async def on_message_delete(message):
    messageList = [message]
    requestMemberList = [message.author]
    nWordsinMessage = await n_bot_calculator_core.n_countCalculation(messageList, requestMemberList)
    if  nWordsinMessage != 0:
        memberIDString = message.author.name + '#' + str(message.author.discriminator)
        await message.channel.send('Detected deletion of message with the N-Word in it in this channel. By ' + memberIDString + '\n' + 'Original message contents: \"' + message.content + '\"')
discordClient.run('ODc1Nzg0MTkwMTgyOTczNTQx.YRajlg.sklbdMAfFFcQdSSSxl3saLuJkU8')



# So far, the way this seems to work is by having an event loop somewhere in client,
# which constantly listens for events, and invokes callback functions pertaining to the event when one is registered.
# (in the background).

# The await key calls asynchronous functions (i.e. everything in discord.py).
# When python encounters an 'await' call, within a function, it will stop the parent function execution there,
# and do other work until it's ready to continue working on that function (once the await-called thing is done,
# probably). So we can do some parallel work in an easy way.
