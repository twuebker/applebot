import os
import discord

client = discord.Client()


def run():
    print("running client...")
    client.run(os.getenv("TOKEN"))


@client.event
async def on_ready():
    print("We have logged in as user {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("Apple"):
        await message.channel.send("Apple God!")


if '__name__' == '__main__':
    run()
