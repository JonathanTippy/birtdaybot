#!/usr/bin/python3
import discord
from discord.ext import tasks
from datetime import datetime
import sys
import asyncio
import time
import os
import random

RAND_WAIT=False

sleep_time=1

if RAND_WAIT:
    sleep_time=random.uniform(1, 2)





# Set editable variables
BIRTHDAY_FILE_PATH = "birthdays.txt"
BIRTHDAY_RUNINDICATOR_PATH = "/tmp/.birtdaybot-running"
PERMISSIONS_INT = 57189942414928

# set misc variables
TOKEN = os.getenv('DISCORD_TOKEN')
MAIN_BOT=False

ALLOW_CHANNEL_STORE=False
sent_reminders = []
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
list_commands_strings = ["help", "commands", "cmds", "list", "listcommands", "cmd", "!h", "halp", "menu"]

# Create a Discord client
client = discord.Client(intents=discord.Intents.all(), permissions=discord.Permissions(PERMISSIONS_INT))

# Close if another instance is already running on this machine
if os.path.exists(BIRTHDAY_RUNINDICATOR_PATH):
    print("another instance is already running")
    sys.exit(157)
else:
    newfile = open(BIRTHDAY_RUNINDICATOR_PATH, "x")
    newfile.close

# Create birtday file if it doesnt exist
if not os.path.exists(BIRTHDAY_FILE_PATH):
    newfile = open(BIRTHDAY_FILE_PATH, "x")
    newfile.close





#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################






# Get a nice time thats human readable
def get_pretty_time():
    now = datetime.now()
    pretty_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return "\x1b[90m" + pretty_time + "\x1b[0m"


# Read usernames and birthdays from a file
def read_birthdays_from_file(file_path):
    if not os.path.exists(file_path):
        newfile = open(file_path, "x")
        newfile.close
    birthdays = {}
    with open(file_path, "r") as file:
        for line in file:
            username, birthday = line.strip().split(":")
            birthdays[username] = datetime.strptime(birthday, "%m/%d").date()
    return birthdays

birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)


# Remove a birthday from the file, return weather or not it was there already
def remove_birthday(file_path, username):
    if not os.path.exists(BIRTHDAY_FILE_PATH):
        newfile = open(BIRTHDAY_FILE_PATH, "x")
        newfile.close
    returnthing = False
    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(file_path, "w") as f:
        for line in lines:
            if not line.startswith(username):
                f.write(line)
            else:
                returnthing = True

    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines[0].isspace():
        lines.pop()

    with open(file_path, 'w') as file:
        file.writelines(lines)

    return returnthing

# Edit a birthday in a file, return weather or not it was there already
def edit_birthday_in_file(file_path, username, newbday):
    if not os.path.exists(BIRTHDAY_FILE_PATH):
        newfile = open(BIRTHDAY_FILE_PATH, "x")
        newfile.close
    returnthing = False

    
    if remove_birthday(file_path, username):
        returnthing = True

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, "w") as f:
        for line in lines:
            f.write(line.strip("\n") + "\n")

    with open(file_path, "a") as f:
        f.write(username + ":" + newbday + "\n")

    return returnthing

# Check if today is a user's birthday
def is_birthday_today(birthday):
    if birthday is None:
        return False
    now = datetime.now()
    return birthday.month == now.month and birthday.day == now.day


# Check what birthday is next
def get_next_birthday(birthdays:dict):
    times_to_birthdays = []
    birthdays_list = []
    upcoming_birthdays_list = []
    now = datetime.now()
    unix_now = time.time()
    for name, birthday in birthdays.items():
        # Calculate the Unix timestamp of the next birthday
        birthday_unix = int(datetime(now.year, birthday.month, birthday.day).timestamp())
        # If the birthday has already passed this year, calculate the Unix timestamp for next year
        if birthday_unix < unix_now:
            birthday_unix = int(datetime(now.year+1, birthday.month, birthday.day).timestamp())
        # If this is the first birthday checked, set it as the next one
        time_to_birthday = birthday_unix - unix_now
        times_to_birthdays.append(time_to_birthday)
        birthdays_list.append([name, birthday])
        if 518400 < time_to_birthday <= 604800:
            upcoming_birthdays_list.append([name, birthday])
            

    # Calculate the remaining time until the next birthday
    next_birthday = birthdays_list[times_to_birthdays.index(min(times_to_birthdays))]
    return [next_birthday, upcoming_birthdays_list]

# Find the closest birthday to a given birthday
def get_nearest_birthday(birthdays, username):
    deltas_to_birthdays = []
    birthdays_list = []
    now = datetime.now()
    unix_now = time.time()
    user_birthday = birthdays[username]

    user_birthday_unix = int(datetime(now.year, user_birthday.month, user_birthday.day).timestamp())
    # If the birthday has already passed this year, calculate the Unix timestamp for next year
    if user_birthday_unix < unix_now:
        user_birthday_unix = int(datetime(now.year+1, user_birthday.month, user_birthday.day).timestamp())

    for name, birthday in birthdays.items():
        # Calculate the Unix timestamp of the next birthday
        birthday_unix = int(datetime(now.year-1, birthday.month, birthday.day).timestamp())
        if not name == username:
            delta_to_birthday = abs(birthday_unix - user_birthday_unix)
            deltas_to_birthdays.append(delta_to_birthday)
            birthdays_list.append([name, birthday])

        birthday_unix = int(datetime(now.year, birthday.month, birthday.day).timestamp())
        # If the birthday has already passed this year, calculate the Unix timestamp for next year
        if not name == username:
            delta_to_birthday = abs(birthday_unix - user_birthday_unix)
            deltas_to_birthdays.append(delta_to_birthday)
            birthdays_list.append([name, birthday])

        birthday_unix = int(datetime(now.year+1, birthday.month, birthday.day).timestamp())
        
        # If this is the first birthday checked, set it as the next one
        if not name == username:
            delta_to_birthday = abs(birthday_unix - user_birthday_unix)
            deltas_to_birthdays.append(delta_to_birthday)
            birthdays_list.append([name, birthday])
    # Calculate the remaining time until the next birthday
    nearest_birthday = birthdays_list[deltas_to_birthdays.index(min(deltas_to_birthdays))]
    return nearest_birthday



def next_occurance(birthday):
    birthday = birthday[1]
    now = datetime.now()
    unix_now = time.time()
    birthday_next = int(datetime(now.year, birthday.month, birthday.day).timestamp())

    if birthday_next > unix_now:
        birthday_next = datetime(now.year+1, birthday.month, birthday.day).timestamp()

    return datetime.fromtimestamp(birthday_next)




#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################





async def send_message(channel, messagetxt, initiating_message):
    global MAIN_BOT
    global ALLOW_CHANNEL_STORE
    global sent_message

    RESPONDED=False

    print(f"{get_pretty_time()}: A user typed: {initiating_message.content}")

    if MAIN_BOT:

        async for uh_message in channel.history(limit = 1):
            latest_message = uh_message

        if ( (messagetxt != latest_message.content) and ( latest_message == initiating_message or ( initiating_message == "special" ) ) ):
            sent_message = await channel.send(messagetxt)
            RESPONDED=True
            print(f"{get_pretty_time()}: Responded.")
        else:
            MAIN_BOT=False
            print(f"{get_pretty_time()}: Undercut, no longer main bot.")
    else:
        ALLOW_CHANNEL_STORE=False
        await asyncio.sleep(sleep_time)  
       
        async for uh_message in channel.history(limit = 1):
            latest_message = uh_message
        
        if ( (messagetxt != latest_message.content) and ( latest_message == initiating_message or ( initiating_message == "special" ) ) ):
            sent_message = await channel.send(messagetxt)
            RESPONDED=True
            print(f"{get_pretty_time()}: Responded; Taking over.")
            MAIN_BOT=True
        else:
            print(f"{get_pretty_time()}: Not responding. Already handled.")

    pileup = 0
    count = 0
    async for the_message in channel.history(limit = 10):

        if ( latest_message.content == the_message.content ):
            if count > 0:
                pileup += 1
        else:
            if count > 0:
                break
        latest_message = the_message
        count += 1

    if RESPONDED:
        if pileup > 0:
            print(f"{get_pretty_time()}: Pileup detected: {pileup}.")
            ALLOW_CHANNEL_STORE=False
            if latest_message == sent_message:
                print(f"{get_pretty_time()}: This instance was fastest.")
                ALLOW_CHANNEL_STORE=True
            else:
                MAIN_BOT=False
                print(f"{get_pretty_time()}: Another instance was faster; deleting response.")
                await sent_message.delete()
        else:
            if latest_message == sent_message:
                ALLOW_CHANNEL_STORE=True

    if ALLOW_CHANNEL_STORE:
      
        for guild in client.guilds:
            channel = discord.utils.get(guild.channels, name="birtday-bot-data")

            async for umm_message in channel.history(limit = 1):
                birthdays_message = umm_message.content.rstrip("\n")


            response = ""

            birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
            for member in channel.guild.members:
                desired_bday = member.name
                if desired_bday in birthdays:
                    parsed_date = birthdays[desired_bday]
                    formatted_date = parsed_date.strftime('%m/%d')
                    response += format(f"{desired_bday}:{formatted_date}\n")

            birthdays_string = response.rstrip("\n")

            if (birthdays_message != birthdays_string):
                await channel.send(birthdays_string)

            


async def birtday_reminder():
    global sent_reminders
    birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
    now = datetime.now()
    for guild in client.guilds:
        channel = discord.utils.get(guild.channels, name="announcements")
        print(f"{get_pretty_time()}: Checking for upcoming birtdays in {guild}.")
        for member in guild.members:
            for upcoming_birtday in get_next_birthday(birthdays)[1]:
                if upcoming_birtday[0] == member.name:
                    if not member.name in sent_reminders:
                        sent_reminders.append(member.name)
                        await send_message(channel, f"@everyone can you believe it guys? {member.name}'s birthday is in a week! im so happy about this information!", "special")
                    

async def check_birthdays_once():
    birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
    now = datetime.now()
    for guild in client.guilds:
        role = discord.utils.get(guild.roles, name="BIRTDAY")
        print(f"{get_pretty_time()}: Checking for birthdays in {guild}.")
        for member in guild.members:
            if is_birthday_today(birthdays.get(member.name)): # Check if it's the user's birthday
                if role is not None: # Check if "BIRTHDAY" role exists
                    if role not in member.roles:
                        await member.add_roles(role) # Assign "BIRTHDAY" role to the member
                        print(f"{get_pretty_time()}: {member.name} has been assigned the 'BIRTHDAY' role.")
            else:
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f"{get_pretty_time()}: The 'BIRTHDAY' role as been removed from {member.name}.")
    if len(birthdays) >= 1:
        await birtday_reminder()
    else:
        print(f"{get_pretty_time()}: No birthdays in file.")







#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################################################################################################################################################################################





# Check birthdays every day, started right after midnight
@tasks.loop(hours=24) # Runs every 24 hours
async def check_birthdays_forever():

    await check_birthdays_once()

# Event: Bot is ready
@client.event
async def on_ready():
    print(f"{get_pretty_time()}: Logged on as {client.user.name}.")

    await check_birthdays_once()
    seconds_until_tomorrow = (86401 - ((time.time() - 18000) % 86400))
    print(f"{get_pretty_time()}: Starting birthday role task.")

#### CHECK FOR CHANGES

    for guild in client.guilds:
        channel = discord.utils.get(guild.channels, name="birtday-bot-data")

        async for uh_message in channel.history(limit = 1):
            birthdays_message = uh_message.content
        
        response = ""

        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        for guild in client.guilds:
            for member in guild.members:
                desired_bday = member.name
                if desired_bday in birthdays:
                    parsed_date = birthdays[desired_bday]
                    formatted_date = parsed_date.strftime('%m/%d')
                    response += format(f"{desired_bday}:{formatted_date}\n")

        birthdays_string = response.rstrip("\n")

        if (birthdays_message != birthdays_string):     
            print(f"{get_pretty_time()}: Updating local birthdays file.")
            with open(BIRTHDAY_FILE_PATH, 'w') as file:
                file.writelines(birthdays_message.rstrip("\n"))
                birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        else:
            print(f"{get_pretty_time()}: Local birthdays file was already up to date.")


    await asyncio.sleep(seconds_until_tomorrow)
    check_birthdays_forever.start()

# Event: bot loses its connection
@client.event
async def on_disconnect():
    
    MAIN_BOT=False
    print(f"{get_pretty_time()}: Connection lost.")


# Event: Message is received

@client.event
async def on_message(message):

    birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)

    if message.channel.name == "birtday-bot-data":
        for guild in client.guilds:
            channel = discord.utils.get(guild.channels, name="birtday-bot-data")

            async for uh_message in channel.history(limit = 1):
                birthdays_message = uh_message.content

        with open(BIRTHDAY_FILE_PATH, 'w') as file:
            file.writelines(birthdays_message.rstrip("\n"))
            birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)

    

    # Cancel if wrong channel
    if message.channel.name != "birtday-bot":
        return
    
    # Cancel if the bot is the author of the message
    if message.author == client.user:
        return
        ##toad: check if it was a list and if it was scrape the info

    # Check if the message starts with the command prefix
    if message.content.startswith("!mybday"):
        print(f'{get_pretty_time()}: Responding to !mybday for {message.author.name}.')
        username = message.author.name
        if username in birthdays:
            birthday_string = months[int(birthdays[username].strftime('%m')) - 1] + " " + birthdays[username].strftime('%d').lstrip("0") + "."
            print(f"{get_pretty_time()}: {username}'s birthday is {birthday_string}.")
            await send_message(message.channel, f"Your birthday is {birthday_string} \nPlease use !editbday if that is not correct.", message)
        else:
            print(f"{get_pretty_time()}: {username} wasn't on record.")
            await send_message(message.channel, "You're not on record. If you would like to provide your birthday, you can use !editbday", message)

    elif message.content.startswith("!nextbday"):
        print(f'{get_pretty_time()}: responding to !nextbday for {message.author.name}.')
        if len(birthdays) >= 1:
            next_birthday = get_next_birthday(birthdays)[0]
        else:
            await send_message(message.channel, f"There are no birthdays in the file.", message)
            return
        birthday_string = months[int(next_birthday[1].strftime('%m')) - 1] + " " + next_birthday[1].strftime('%d').lstrip("0") + "."
        print(f"{get_pretty_time()}: The next birthday is {next_birthday[0]}'s birthday which falls on {birthday_string}.")
        await send_message(message.channel, f"The next birthday is {next_birthday[0]}'s birthday which falls on {birthday_string}", message)

    elif message.content.startswith("!closestbday"):
        print(f'{get_pretty_time()}: Responding to !closestbday for {message.author.name}.')
        username = message.author.name
        user_birthday = birthdays.get(message.author.name)
        if not user_birthday:
            print(f"{get_pretty_time()}: {username} wasn't on record.")
            await send_message(message.channel, "You're not on record. If you would like to provide your birthday, you can use !editbday", message)
        else:
            
            birthday_string = months[int(birthdays[username].strftime('%m')) - 1] + " " + birthdays[username].strftime('%d').lstrip("0") + "."
            if len(birthdays) >= 1:
                nearest_birthday = get_nearest_birthday(birthdays, message.author.name)
            else:
                await send_message(message.channel, f"There are no birthdays in the file.", message)
                return
            birthday_string_2 = months[int(nearest_birthday[1].strftime('%m')) - 1] + " " + nearest_birthday[1].strftime('%d').lstrip("0") + "."

            print(f"{get_pretty_time()}: {username}'s birthday is {birthday_string}.")
            await send_message(message.channel, f"Your birthday is {birthday_string} \nPlease use !editbday if that is not correct.\nThe closest birthday is {nearest_birthday[0]}'s birthday which falls on {birthday_string_2}", message)

    elif message.content.startswith("!editbday"):
        print(f'{get_pretty_time()}: Responding to !editbday for {message.author.name}.')
        username = message.author.name
        response = ""
        if username in birthdays:
            birthday_string = months[int(birthdays[username].strftime('%m')) - 1] + " " + birthdays[username].strftime('%d').lstrip("0") + "."
            response += f'Your birthday is currently {birthday_string}\n'
            response += "Please enter your new birthday in the format MM/DD, for example, 12/31. Type quit to cancel. Type remove if you want your birthday removed."
        else:
            response += "You're not on record yet.\n"
            response += "Please enter your birthday in the format MM/DD, for example, 12/31. Type quit to cancel."

        await send_message(message.channel, response, message)

        ## THIS IS USED IN WAIT FOR MESSAGE DO NOT REMOVE

        def check(m):
            if m.author == message.author and m.channel == message.channel:
                if m.content.startswith("quit") or m.content.startswith("remove"):
                    return True
                parts = m.content.split("/")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    month = int(parts[0])
                    day = int(parts[1])
                    if month >= 1 and month <= 12 and day >= 1 and day <= 31:
                        return True
            return False

        try:
            newbday_message = await client.wait_for('message', check=check, timeout=300)
        except:
            await send_message(message.channel, 'Timed out. (5 minutes) If you want, try again with !editbday', message)
            return

        if not (newbday_message.content == "quit" or newbday_message.content == "remove"):
            if edit_birthday_in_file(BIRTHDAY_FILE_PATH, username, newbday_message.content):
                print(f"{get_pretty_time()}: {message.author.name} changed their birthday to {newbday_message.content}.")
                await send_message(newbday_message.channel, 'Birthday successfully edited.', newbday_message)
                await check_birthdays_once()
            else:
                print(f"{get_pretty_time()}: {message.author.name} set their birthday to {newbday_message.content}.")
                await send_message(newbday_message.channel, 'Birthday successfully added.', newbday_message)
                await check_birthdays_once()
        elif newbday_message.content == "quit":
            print(f"{get_pretty_time()}: {message.author.name} cancelled the edit.")
            await send_message(newbday_message.channel, 'Cancelled.', newbday_message)
        elif newbday_message.content == "remove":
            if remove_birthday(BIRTHDAY_FILE_PATH, username):
                print(f"{get_pretty_time()}: Removed {message.author.name}'s birthday from the file.")
                await send_message(newbday_message.channel, 'Your birthday has been removed.', newbday_message)
                await check_birthdays_once()
            else:
                await send_message(newbday_message.channel, "Silly, you aren't on the list so you can't be removed.", newbday_message)

    elif message.content.startswith("!getbday"):
        print(f'{get_pretty_time()}: Responding to !getbday for {message.author.name}.')
        username = message.author.name
        await send_message(message.channel, "Please provide a username, or quit to cancel. If you don't know the exact username, use !listbday. If you just want your own birthday, use !mybday", message)

        ## THIS IS USED IN WAIT FOR MESSAGE DO NOT REMOVE

        def check(m):
            if m.author == message.author and m.channel == message.channel:
                return True
            elif m.content == "quit":
                return True
            else:
                return False

        try:
            username_message = await client.wait_for('message', check=check, timeout=300)
        except:
            await send_message(message.channel, 'Timed out. (5 minutes) If you want, try again with !getbday', message)
            return

        if username_message.content == "quit":
            print(f"{get_pretty_time()}: {message.author.name} cancelled the get.")
            await send_message(username_message.channel, 'Cancelled.', username_message)
            return

        desired_bday = username_message.content

        if desired_bday in birthdays:
            birthday_string = months[int(birthdays[desired_bday].strftime('%m')) - 1] + " " + birthdays[desired_bday].strftime('%d').lstrip("0") + "."
            print(f"{get_pretty_time()}: {desired_bday}'s birthday is {birthday_string}.")
            await send_message(username_message.channel, f"{desired_bday}'s birthday is {birthday_string}", username_message)
        else:
            print(f"{get_pretty_time()}: {desired_bday} wasn't on record.")     
            await send_message(username_message.channel, f"{desired_bday} wasn't on record", username_message)   

    elif message.content.startswith("!listbday"):
        print(f'{get_pretty_time()}: Responding to !listbday for {message.author.name}.')
        response = ""
         
        for birthday in birthdays:
            birthday_string = months[int(birthdays[birthday].strftime('%m')) - 1] + " " + birthdays[birthday].strftime('%d').lstrip("0") + "."
            print(f"{get_pretty_time()}: {birthday}'s birthday is {birthday_string}.")
            response += format(f"{birthday}'s birthday is {birthday_string}\n")



        await send_message(message.channel, response.rstrip("\n"), message)
        
    elif any(command in message.content for command in list_commands_strings):
        print(f'{get_pretty_time()}: Responding to commands query for {message.author.name}.')
        await send_message(message.channel, f"The valid commands are as follows: !mybday, !nextbday, !closestbday, !editbday, !getbday, !listbday.\n For more informantion, visit <#1098480931439915058>", message)

# Run the bot with your Discord bot token

client.run(TOKEN)

