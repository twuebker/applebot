import os
import discord
import war_track

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def run():
  print("running client...")
  token = os.environ['TOKEN']
  client.run(token)


@client.event
async def on_ready():
  print("We have logged in as user {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("$Who is Ace?"):
    await message.channel.send("Ace is the best coc player ever!")
  if message.content.startswith("$Track"):
    tag = message.content.split("$Track ", 1)[1]
    war_msg = war_track.print_war(tag)
    await message.channel.send(war_msg)


if '__name__' == '__main__':
  run()
