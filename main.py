import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def run():
  print("running client...")
  token = os.getenv('TOKEN')
  if token is None:
    return
  client.run(token=token)


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
