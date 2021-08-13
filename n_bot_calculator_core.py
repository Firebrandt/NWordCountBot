import discord
nWordHardR = 'nigger'

# This code file does most of the background calculations for the bot's interface segment,
# and then hands it the result.
async def n_countCalculation(messageList, requestMemberList): #TODO: rename this to member.
    memberCounts = {}
    for member in requestMemberList:
        memberCounts.update({member.name + '#' + member.discriminator: 0})

    for message in messageList:
        if message.author in requestMemberList and nWordHardR in message.content:
            memberCounts[message.author.name + '#' + message.author.discriminator] += 1

    return memberCounts





