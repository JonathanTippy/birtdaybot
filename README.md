# birtdaybot
a gratuitously distributed discord bot that manages birthdays. Its like this so you can use multiple computers around your house
to gurentee it stays up even if you shut off all but one.

# operation
on first interaction each instance sends a response to find out what one is the fastest. 
The slower ones delete their replies. After that, it should be responsive and only respond once.

# usage
to use it; create a bot using discord dev page, get a token from the discord dev page and set it to DISCORD_TOKEN in your environment, by adding export DISCORD_TOKEN=<token> to your .profile. Then enable all of the privelidged gateway intents on the discord dev page, then use this link to invite it to your server.  (FILL IN BOT ID):
https://discord.com/api/oauth2/authorize?client_id=<bot id>&permissions=57189942414928&scope=bot
you will need to make a "BIRTDAY" (that is not a typo, thats just what it is.) role, and a birtday-bot channel. 
Also a birtday-bot-data channel which should be only visible to birtdaybot (though it doesnt have to be)
now just make sure you have your token on all your machines and set the bash file to run on startup.

commands:

!mybday

check your current birthday in the file

!listbday

check the birthdays of every user

!nextbday

find out the next birthday

!getbday

find out the birthday of any user

!closestbday

find out whos birthday is closest to yours

!editbday

set your birthday, change it if you made a mistake, or remove it from the system.
