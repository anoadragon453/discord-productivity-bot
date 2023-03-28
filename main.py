import os
import sys
import asyncio
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

TOKEN = os.environ.get("PRODUCTIVITY_BOT_TOKEN")
if not TOKEN:
    print(
        "You must provide a token via an environment variable "
        "called 'PRODUCTIVITY_BOT_TOKEN'. Exiting."
    )
    sys.exit(1)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# A map of member ID to minutes they've spent in voice.
user_voice_time = {}

# The users to track. Convert each to an int.
users_to_track = os.environ.get("PRODUCTIVITY_BOT_USERS_TO_TRACK", "").split(",")
users_to_track = [
    int(member_id)
    for member_id in users_to_track
]
if not users_to_track:
    print(
        "You must specify at least one member ID to track via an "
        "environment variable called 'PRODUCTIVITY_BOT_USERS_TO_TRACK'. "
        "Exiting."
    )
    sys.exit(1)
print("Tracking the following users:", users_to_track)

# The number of minutes to allow users to be in voice channels each day.
# Defaults to 180 minutes, or 3 hours.
try:
    MAXIMUM_MINUTES = int(os.environ.get("PRODUCTIVITY_BOT_MAX_MINUTES", 180))
except ValueError:
    print("'PRODUCTIVITY_BOT_MAX_MINUTES' is not a valid integer. Exiting.")
    sys.exit(1)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    monitor_voice_channels.start()
    reset_voice_time_daily.start()


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id not in users_to_track:
        print(f"Member ID {member.id} not in tracked user list. Ignoring.")
        return


@tasks.loop(seconds=60)
async def monitor_voice_channels():
    for guild in bot.guilds:
        for member in guild.members:
            if member.id not in users_to_track:
                continue

            if member.voice is not None and member.voice.channel is not None:
                if member.id not in user_voice_time:
                    user_voice_time[member.id] = 0
                    print("Now tracking member with ID:", member.id)

                user_voice_time[member.id] += 1
                remaining_minutes = MAXIMUM_MINUTES - user_voice_time[member.id]

                print(
                    f"Member '{member.id}' currently has "
                    f"{remaining_minutes} minutes remaining."
                )

                # Warn the user that they are about to run out of minutes.
                if remaining_minutes == 10:
                    if user := bot.get_user(member.id):
                        await user.send(f"You will be disconnected from your current voice channel in 10 minutes.")
                        print(f"Informed {member.id} that they will be disconnected in 10 minutes.")

                # Disconnect the user if they have been in a call for more than 3 hours (180 minutes)
                if remaining_minutes <= 0:
                    print(f"Disconnecting user {member.id}")
                    await member.move_to(None, reason="Daily voice call limit reached. Sorry!")


@tasks.loop(hours=24)
async def reset_voice_time_daily():
    """Clears everyone's tracked hours daily at midnight local time."""
    user_voice_time.clear()


@reset_voice_time_daily.before_loop
async def before_reset_voice_time_daily():
    """Called once before the reset_voice_time_daily function begins to loop
    to ensure that the loop kicks off at midnight.
    """
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    await asyncio.sleep((midnight - now).seconds)


bot.run(TOKEN)
print(
    "You can add me to your server by clicking the following link:"
    f"https://discord.com/api/oauth2/authorize?client_id={bot.application_id}"
    "&permissions=16780288&scope=bot%20applications.commands"
)