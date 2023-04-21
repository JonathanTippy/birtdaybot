import discord
from discord.ext import tasks, commands
from datetime import datetime
import asyncio
import time
import os

BIRTHDAY_FILE_PATH = "birthdays.txt"
TOKEN = os.getenv('DISCORD_TOKEN')
PERMISSIONS_INT = 57189942414928

# Create a Discord client

client = discord.Client(intents=discord.Intents.all())

PERMISSIONS_INT = 57189942414928
permissions = discord.Permissions(PERMISSIONS_INT)

client.permissions = permissions

if not os.path.exists(BIRTHDAY_FILE_PATH):
    newfile = open(BIRTHDAY_FILE_PATH, "x")
    newfile.close
# Get a nice time thats human readable
def get_pretty_time():
    now = datetime.now()
    pretty_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return "\x1b[90m" + pretty_time + "\x1b[0m"


# Read usernames and birthdays from a file
def read_birthdays_from_file(file_path):
    if not os.path.exists(BIRTHDAY_FILE_PATH):
        newfile = open(BIRTHDAY_FILE_PATH, "x")
        newfile.close
    birthdays = {}
    with open(file_path, "r") as file:
        for line in file:
            username, birthday = line.strip().split(":")
            birthdays[username] = datetime.strptime(birthday, "%m/%d").date()
    return birthdays

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

    if lines[-1].isspace():
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
            f.write(line)
        f.write(username + ":" + newbday)

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
async def birtday_reminder():
    birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
    now = datetime.now()
    for guild in client.guilds:
        channel = discord.utils.get(guild.channels, name="birtday-bot")
        print(f"{get_pretty_time()}: checking for upcoming birtdays in {guild}")
        for member in guild.members:
            for upcoming_birtday in get_next_birthday(birthdays)[1]:
                if upcoming_birtday[0] == member.name:
                    await channel.send(f"can you believe it guys? {member.name}'s birthday is in a week! im so happy about this information!")
                    

async def check_birthdays_once():
    birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
    now = datetime.now()
    for guild in client.guilds:
        role = discord.utils.get(guild.roles, name="BIRTDAY")
        print(f"{get_pretty_time()}: checking for birthdays in {guild}")
        for member in guild.members:
            #print(member)
            if is_birthday_today(birthdays.get(member.name)): # Check if it's the user's birthday
                if role is not None: # Check if "BIRTHDAY" role exists
                    if role not in member.roles:
                        await member.add_roles(role) # Assign "BIRTHDAY" role to the member
                        print(f"{get_pretty_time()}: {member.name} has been assigned the 'BIRTHDAY' role.")
            else:
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f"{get_pretty_time()}: The 'BIRTHDAY' role as been removed from {member.name}")
    if len(birthdays) >= 1:
        await birtday_reminder()
    else:
        print(f"{get_pretty_time()}: no birthdays in file")


# Check birthdays every day
@tasks.loop(hours=24) # Runs every 24 hours
async def check_birthdays_forever():

    check_birthdays_once()

# Event: Bot is ready
@client.event
async def on_ready():
    print('Logged on as', client.user.name)
    print('------')
    await check_birthdays_once()
    seconds_until_tomorrow = (86401 - ((time.time() - 18000) % 86400))
    print(f"{get_pretty_time()}: sleeping {seconds_until_tomorrow} seconds")
    await asyncio.sleep(seconds_until_tomorrow)
    check_birthdays_forever.start()


# Event: Message is received

@client.event
async def on_message(message):
    if message.channel.name != "birtday-bot":
        return
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Check if the bot is the author of the message
    if message.author == client.user:
        return
    # Check if the message starts with the command prefix
    if message.content.startswith("!mybday"):
        print(f'{get_pretty_time()}: responding to !mybday for {message.author.name}')
        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        username = message.author.name
        if username in birthdays:
            birthday_string = months[int(birthdays[username].strftime('%m')) - 1] + " " + birthdays[username].strftime('%d').lstrip("0") + "."
            print(f"{get_pretty_time()}: {username}'s birthday is {birthday_string}")
            await message.channel.send(f"Your birthday is {birthday_string} \nPlease use !editbday if that is not correct.")
        else:
            print(f"{get_pretty_time()}: {username} wasn't on record")
            await message.channel.send("You're not on record. If you would like to provide your birthday, you can use !editbday")

    elif message.content.startswith("!nextbday"):
        print(f'{get_pretty_time()}: responding to !nextbday for {message.author.name}')
        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        if len(birthdays) >= 1:
            next_birthday = get_next_birthday(birthdays)[0]
        else:
            await message.channel.send(f"There are no birthdays in the file.")
            return
        birthday_string = months[int(next_birthday[1].strftime('%m')) - 1] + " " + next_birthday[1].strftime('%d').lstrip("0") + "."
        print(f"{get_pretty_time()}: The next birthday is {next_birthday[0]}'s birthday which falls on {birthday_string}")
        await message.channel.send(f"The next birthday is {next_birthday[0]}'s birthday which falls on {birthday_string}")

    elif message.content.startswith("!closestbday"):
        print(f'{get_pretty_time()}: responding to !closestbday for {message.author.name}')
        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        username = message.author.name
        user_birthday = birthdays.get(message.author.name)
        if not user_birthday:
            print(f"{get_pretty_time()}: {username} wasn't on record")
            await message.channel.send("You're not on record. If you would like to provide your birthday, you can use !editbday")
        else:
            
            birthday_string = months[int(birthdays[username].strftime('%m')) - 1] + " " + birthdays[username].strftime('%d').lstrip("0") + "."
            if len(birthdays) >= 1:
                nearest_birthday = get_nearest_birthday(birthdays, message.author.name)
            else:
                await message.channel.send(f"There are no birthdays in the file.")
                return
            birthday_string_2 = months[int(nearest_birthday[1].strftime('%m')) - 1] + " " + nearest_birthday[1].strftime('%d').lstrip("0") + "."

            print(f"{get_pretty_time()}: {username}'s birthday is {birthday_string}")
            await message.channel.send(f"Your birthday is {birthday_string} \nPlease use !editbday if that is not correct.\nThe closest birthday is {nearest_birthday[0]}'s birthday which falls on {birthday_string_2}")

    elif message.content.startswith("!editbday"):
        print(f'{get_pretty_time()}: responding to !editbday for {message.author.name}')
        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        username = message.author.name
        if username in birthdays:
            birthday_string = months[int(birthdays[username].strftime('%m')) - 1] + " " + birthdays[username].strftime('%d').lstrip("0") + "."
            await message.channel.send(f'Your birthday is currently {birthday_string}')
        else:
            await message.channel.send("You're not on record yet.")
        await message.channel.send("Please enter your new birthday in the format MM/DD, for example, 12/31. Type quit to cancel. Type remove if you want your birthday removed.")

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
            await message.channel.send('Timed out. (5 minutes) If you want, try again with !editbday')
            return
        
        if not (newbday_message.content == "quit" or newbday_message.content == "remove"):
            if edit_birthday_in_file(BIRTHDAY_FILE_PATH, username, newbday_message.content):
                print(f"{get_pretty_time()}: {message.author.name} changed their birthday to {newbday_message.content}")
                await message.channel.send('Birthday successfully edited.')
                await check_birthdays_once()
            else:
                print(f"{get_pretty_time()}: {message.author.name} set their birthday to {newbday_message.content}")
                await message.channel.send('Birthday successfully added.')
                await check_birthdays_once()
        elif newbday_message.content == "quit":
            print(f"{get_pretty_time()}: {message.author.name} cancelled the edit")
            await message.channel.send('Cancelled.')
        elif newbday_message.content == "remove":
            if remove_birthday(BIRTHDAY_FILE_PATH, username):
                print(f"{get_pretty_time()}: removed {message.author.name}'s birthday from the file")
                await message.channel.send('Your birthday has been removed.')
                await check_birthdays_once()
            else:
                await message.channel.send("Silly, you aren't on the list so you can't be removed.")

    elif message.content.startswith("!getbday"):
        print(f'{get_pretty_time()}: responding to !getbday for {message.author.name}')
        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        username = message.author.name
        await message.channel.send("Please provide a username, or quit to cancel. If you don't know the exact username, use !listbday. If you just want your own birthday, use !mybday")
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
            await message.channel.send('Timed out. (5 minutes) If you want, try again with !getbday')
            return

        if username_message.content == "quit":
            print(f"{get_pretty_time()}: {message.author.name} cancelled the get")
            await message.channel.send('Cancelled.')
            return

        desired_bday = username_message.content

        if desired_bday in birthdays:
            birthday_string = months[int(birthdays[desired_bday].strftime('%m')) - 1] + " " + birthdays[desired_bday].strftime('%d').lstrip("0") + "."
            print(f"{get_pretty_time()}: {desired_bday}'s birthday is {birthday_string}")
            await message.channel.send(f"{desired_bday}'s birthday is {birthday_string}")
        else:
            print(f"{get_pretty_time()}: {desired_bday} wasn't on record")     
            await message.channel.send(f"{desired_bday} wasn't on record")   

    elif message.content.startswith("!listbday"):
        print(f'{get_pretty_time()}: responding to !listbday for {message.author.name}')
        response = ""

        birthdays = read_birthdays_from_file(BIRTHDAY_FILE_PATH)
        for member in message.guild.members:
            desired_bday = member.name
            if desired_bday in birthdays:
                birthday_string = months[int(birthdays[desired_bday].strftime('%m')) - 1] + " " + birthdays[desired_bday].strftime('%d').lstrip("0") + "."
                print(f"{get_pretty_time()}: {desired_bday}'s birthday is {birthday_string}")
                response += format(f"{desired_bday}'s birthday is {birthday_string}\n")
            else:
                print(f"{get_pretty_time()}: {desired_bday} wasn't on record")     
                response += format(f"{desired_bday} wasn't on record\n")   

        await message.channel.send(response)
        

# Run the bot with your Discord bot token

#check_birthdays.before_loop(client.wait_until_ready())    

client.run(TOKEN)