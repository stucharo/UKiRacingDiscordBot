import os
import requests

import discord

class iRacing:

    def __init__(self):
        self.session = requests.Session()
        self.login()

    def login(self):
        loginUrl = "https://members.iracing.com/download/Login?"
        creds = {
            "username": os.getenv("IRACING_USERNAME"),
            "password": os.getenv("IRACING_PASSWORD"),
        }
        self.session.post(loginUrl, creds)


    async def get_driver_status(self, name):
        payload = {"searchTerms": name}
        d = self.session.get(
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
        ir = iRacing()
        ds = await ir.get_driver_status(message.author.display_name)

        #await message.channel.send(f"{d.json()}")
        await message.channel.send(f"custID = {ds['custid']}")

client.run(DISCORD_TOKEN)
