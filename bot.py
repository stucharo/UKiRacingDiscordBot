import os
import requests

import discord


def get_iRacing_session():
    loginUrl = "https://members.iracing.com/download/Login?"
    creds = {
        "username": os.getenv("IRACING_USERNAME"),
        "password": os.getenv("IRACING_PASSWORD"),
    }
    s = requests.Session()
    s.post(loginUrl, creds)
    return s


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
        payload = {"searchTerms": message.author.display_name}
        s = get_iRacing_session()
        d = s.get(
            "https://members.iracing.com/membersite/member/GetDriverStatus",
            params=payload,
        )
        await message.channel.send(f"{d.json()}")


client.run(DISCORD_TOKEN)
