import discord

nWordTypes = ['NIGGA', 'NIGA', 'NIGGE', 'NIGGR', 'NIGR', 'NIGGUR', 'NEGRO', 'NGR', 'NIGGER']
discordClient = discord.Client()


# This code file does most of the background calculations for the bot's interface segment,
# and then hands it the result.


async def message_search(requestGuildTxtChannels, requestUserList):
    # put the messages from every channel into a gigantic list (will probably take a while T_T)
    messageList = []

    for text_channel in requestGuildTxtChannels:
        channelMessageList = await text_channel.history().flatten()
        messageList += channelMessageList
        # after grabbing messages, we send this to the calculator function

    return await n_countCalculation(messageList, requestUserList)


async def n_countCalculation(messageList, requestMemberList):
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
                    memberCounts[message.author.name + '#' + message.author.discriminator] += 1

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
    gSubList = ['B', 'C', 'C;', 'g', '🤙', '☪', '↪', '🇬', 'b', '🅱️']
    for gSub in gSubList:
        messageText = messageText.replace(gSub, 'G')

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

    return messageText


# Removes special characters (and spaces and newlines) from the string.
async def remove_special_characters(message):
    messageText = message
    for thisChar in messageText:
        if not (ascii(thisChar) >= ascii(0) and ascii(thisChar) <= ascii(9) or ascii(thisChar) >= ascii('A') and ascii(
                thisChar) <= ascii('Z')):
            messageText = messageText.replace(thisChar, '')

    return messageText

    # TODO: Maybe optimize list - do one, store pairs for replacement ID? Could be faster than having 1 mil. Less organized tho.
