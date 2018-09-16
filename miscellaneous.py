import discord
import datetime
from datetime import datetime
import dynamo

default_suggestion_wait = 6


async def invite_link(message):
    await message.channel.send("https://discord.gg/ErTb8t3")
    return


async def custom(message):
    try:
        parsed = message.content.split()
        if len(parsed) < 2:
            raise Exception()
        command = parsed[1]
        value = ""
        for part in parsed[2:]:
            value += part + " "
        if dynamo.add_custom_command(command, value) == "deleted":
            await message.channel.send("Command deleted!")
        else:
            await message.channel.send("Mission Accomplished")
    except Exception as e:
        print(e)
        await message.channel.send("Invalid Command")
    return


async def help(message):
    msg = "**$cone <@user1> <@user2> ...**"
    msg += "\n**$uncone <@user1> <@user2> ...**"
    msg += "\n**$mute <@user1> <@user2> ...**"
    msg += "\n**$unmute <@user1> <@user2> ...**"
    msg += "\n**$servermute <@user1> <@user2> ...** (server-wide mute)"
    msg += "\n**$serverunmute <@user1> <@user2> ...** (server-wide unmute)"
    msg += "\n**$clear <#> <@user>** (optionally specify a user to only target him/her)"
    msg += "\n**$invitelink** (prints an invite to MG)"
    msg += "\n**$custom <command> <msg to be sent>** (creates/updates a custom command)"
    msg += "\n**$custom <command>** (deletes an existing command)"
    msg += "\n**$mutechannel** (mutes everyone except for mods)"
    msg += "\n**$unmutechannel** (brings the channel back to how it was)"
    await message.channel.send(msg)


async def new_suggestion(message, client, suggestions_chat):
    date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    latest_sugg = dynamo.get_latest_suggestion(message)
    if latest_sugg is not None:
        old_date = datetime.strptime(latest_sugg['date'], "%Y-%m-%d %H:%M:%S")
        date_delta = abs(date - old_date)
        if date_delta.days <= 0 and date_delta.seconds / 3600 < default_suggestion_wait:
            await message.author.send(
                "Too soon! You need to wait " + str(
                    default_suggestion_wait * 60 - int(date_delta.seconds / 60)) + " minutes.")
            return
    dynamo.add_new_suggestion(message, date)
    await client.get_channel(suggestions_chat).send("New Suggestion: " + message.content[message.content.find(' '):])
    await message.author.send("Thanks for your suggestion!")
    return
