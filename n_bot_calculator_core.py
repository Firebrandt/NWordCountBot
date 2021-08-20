import discord

nWordTypes = ['NIGGA', 'NIGGE', 'NIGGR', 'NIGR', 'NIGGUR', 'NEGRO', 'NIGAS', ' NIGA', ' NGR', ' NIG NOG']
discordClient = discord.Client()
myDiscordID = 186540780603703296


# This code file does most of the background calculations for the bot's interface segment,
# and then hands it the result. It does do a handful of status message outputs.


async def message_search(requestGuildTxtChannels, requestUserList, requestChannel):
    # put the messages from every channel into a gigantic list (will probably take a while T_T)
    messageList = []

    for text_channel in requestGuildTxtChannels:
        #Rate limit = 50 per second
        channelMessageList = await text_channel.history(limit=100000).flatten()
        print(len(channelMessageList))
        messageList += channelMessageList
        # after grabbing messages, we send this to the calculator function
    await requestChannel.send('Grabbed messages. Processing now.')
    return await n_countCalculation(messageList, requestUserList, requestChannel, "count N words")

#Count the number of N-Words in a message. If being called as part of N_count (and not just to count in a single message), for functions like N_edit, it will mark found messages.
async def n_countCalculation(messageList, requestMemberList, requestChannel, useFlag):
    # set up member counts return thing.
    memberCounts = {}
    for member in requestMemberList:
        memberCounts.update({member.name + '#' + member.discriminator: 0})

    for message in messageList:
        # run the processing functions.
        messageText = message.content
        messageText1 = await remove_replacement(messageText)
        messageText2 = await remove_duplicates(messageText1)
        messageTextFinal = await remove_special_characters(messageText2)

        #Increment N-word count for requested members, if one is spotted.
        if message.author in requestMemberList:
            for nWord in nWordTypes:
                if nWord in messageTextFinal:
                    memberIDString = message.author.name + '#' + str(message.author.discriminator)
                    memberCounts[memberIDString] += messageTextFinal.count(nWord)
                    if message.author.id != myDiscordID+69 and useFlag == "count N words":
                        await message.reply('📸')
                        await message.channel.send('Original message (failsafe output): "' + message.content + '" ' + memberIDString)
                    #await  requestChannel.send('what the bot sees: ' + messageTextFinal)

    return memberCounts


# processes the message to properly detect the N-Word. Or at least, allows for processing.
# The following functions will perform a processing step on a string, then return the modified version. Chain them together.
async def remove_replacement(message):
    messageText = message
    # Deal with N-Replacements.
    nSubList = ['/\\\\/', '|\\\\|', 'I\\\\I', '!\\\\!', 'l\\\\l', 'n', '🇳']
    for nSub in nSubList:
        messageText = messageText.replace(nSub, 'N')

    # Deal with I-Replacements.
    iSubList = ['1', 'l', '|', '[]', '{}', '!', 'J', '?', 'i', 'ℹ', '❗', '❕', '🇮']
    for iSub in iSubList:
        messageText = messageText.replace(iSub, 'I')

    # Deal with G-Replacements.
    gSubList = ['BB', 'C;', 'g', '🤙', '☪', '↪', '🇬', 'bb', '🅱️']
    for gSub in gSubList:
        if len(gSub) == 1:
            messageText = messageText.replace(gSub, 'G')
        elif len(gSub) == 2:
            messageText = messageText.replace(gSub, 'GG')

    # Deal with E-Replacements.
    eSubList = ['e', 'U', '3', '🇪']
    for eSub in eSubList:
        messageText = messageText.replace(eSub, 'E')

    # Deal with R-Replacements.
    rSubList = ['r', '🇷']
    for rSub in rSubList:
        messageText = messageText.replace(rSub, 'R')

    # Deal with A-Replacements
    aSubList = ['a', '4', '@', '4️⃣']
    for aSub in aSubList:
        messageText = messageText.replace(aSub, 'A')

    #print('replacements cut: ' + messageText)
    return messageText


# Removes duplicate characters. Kinda yucky, but python is immutable. -_-.
async def remove_duplicates(message):
    messageText = message
    while ('NN' in messageText):
        messageText = messageText.replace('NN', 'N')

    while ('II' in messageText):
        messageText = messageText.replace('II', 'I')

    while ('GGG' in messageText):
        messageText = messageText.replace('GGG', 'GG')

    while ('EE' in messageText):
        messageText = messageText.replace('EE', 'E')

    while ('RR' in messageText):
        messageText = messageText.replace('RR', 'R')

    #print('duplicates cut: ' + messageText)
    return messageText


# Removes special characters (and spaces and newlines) from the string. Oh, and add a space at string start (for proper detection there)
async def remove_special_characters(message):
    messageText = message
    for index in range(0, len(messageText)-1):
        #This operation reduces string length, hence we need an extra check to avoid index error here.
        if index <= len(messageText)-1:
            thisChar = messageText[index]
            if not (ascii(thisChar) >= ascii(0) and ascii(thisChar) <= ascii(9) or ascii(thisChar) >= ascii('A') and ascii(
                    thisChar) <= ascii('Z') or ascii(thisChar) >= ascii('a') and ascii(thisChar) <= ascii('z')):
                #Ignore " N" here because it helps us search for unattached N-word candidates (useful for less certain spellings)
                if not (index+1 <= len(messageText)-1 and ascii(thisChar) == ascii(' ') and ascii(messageText[index+1] == ascii('N'))):
                    #print("substring:" + messageText[index:index+1])
                    messageText = messageText.replace(thisChar, '')

    messageText = messageText.rjust(20)
    #print('specials cut: ' + messageText)
    return messageText

    # TODO: Maybe optimize list - do one, store pairs for replacement ID? Could be faster than having 1 mil. Less organized tho.
