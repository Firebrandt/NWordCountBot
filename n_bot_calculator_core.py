import discord
nWordHardR = 'nigger'
discordClient = discord.Client()

# This code file does most of the background calculations for the bot's interface segment,
# and then hands it the result.


async def message_search(requestGuildTxtChannels, requestUserList):
    #put the messages from every channel into a gigantic list (will probably take a while T_T)
    messageList = []

    for text_channel in requestGuildTxtChannels:
       channelMessageList = await text_channel.history().flatten()
       messageList += channelMessageList
       # after grabbing messages, we send this to the background since we really don't need the client at this point.

    return await n_countCalculation(messageList, requestUserList)

async def n_countCalculation(messageList, requestMemberList):
    memberCounts = {}
    for member in requestMemberList:
        memberCounts.update({member.name + '#' + member.discriminator: 0})

    for message in messageList:
        if message.author in requestMemberList and nWordHardR in message.content:
            memberCounts[message.author.name + '#' + message.author.discriminator] += 1

    return memberCounts





