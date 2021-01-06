import os
import requests

import discord


async def get_iRacing_session():
    loginUrl = "https://members.iracing.com/download/Login?"
    creds = {
        "username": os.getenv("IRACING_USERNAME"),
        "password": os.getenv("IRACING_PASSWORD"),
    }
    s = requests.Session()
    s.post(loginUrl, creds)
    return s


async def get_driver_status(session, name):
    payload = {"searchTerms": name}
    d = session.get(
        "https://members.iracing.com/membersite/member/GetDriverStatus",
        params=payload,
    )
    drivers = d.json()["searchRacers"]
    
    return next(driver for driver in drivers if driver["name"] == name.replace(" ", "+"))


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    # Prevent event being raised when the bot posts a message
    if message.author == client.user:
        return

    if message.content == "$iRacing":
        s = await get_iRacing_session()
        d = await get_driver_status(s, message.author.display_name)

        #await message.channel.send(f"{d.json()}")
        print(f"custID = {d['custid']}")

client.run(DISCORD_TOKEN)
