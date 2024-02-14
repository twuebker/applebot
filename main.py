import os
import discord
import requests
from dotenv import load_dotenv
import json
from discord import Embed

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
api_url = "https://libretranslate.eownerdead.dedyn.io/translate"
emoji_flag_to_country_code = {
    "🇩🇪": "de",
    "🇺🇸": "en",
    "🇬🇧": "en",
    "🇫🇷": "fr",
    "🇮🇹": "it",
    "🇨🇳": "zh",
    "🇮🇳": "hi",
    "🇧🇷": "br",
    "🇷🇺": "ru",
    "🇯🇵": "ja",
    "🇫🇮": "fi",
    "🇸🇪": "sv",
    "🇳🇱": "nl",
    "🇬🇷": "el",
    "🇳🇴": "nb",
    "🇰🇷" : "ko",
    "🇵🇱" : "pl"
}
country_code_to_emoji_flags = {value: key for key, value in emoji_flag_to_country_code.items()}
environment = {'pw': ""}
verified_servers = []

def run():
    print("running client...")
    load_dotenv()
    token = os.environ['TOKEN']
    environment['pw'] = os.environ['PW']
    client.run(token)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$Login"):
        k = message.content.split("Login ", 1)[1]
        print(k)
        print(environment['pw'])
        if k == environment['pw']:
            server_id = message.guild.id
            verified_servers.append(server_id)
            await message.channel.send(content="Successfully logged in.")

@client.event
async def on_reaction_add(reaction, user):
    server_id = reaction.message.guild.id
    if not server_id in verified_servers:
        await reaction.message.channel.send(content="Please log in.")
        return
    if reaction.emoji in emoji_flag_to_country_code:
        target_lang = emoji_flag_to_country_code[reaction.emoji]
        message = reaction.message.content
        response = send_translation_request(message, target_lang)
        detected_language = response['detectedLanguage']['language']
        translation = response['translatedText']
        embedding, icon = create_embedding(message, translation, detected_language, user.name)
        await reaction.message.channel.send(embed=embedding, file=icon)

def create_embedding(original_msg, translation, detected_lang, user):
    resp = Embed(description=translation, color=0x00ff00)
    resp.add_field(name='Original Message', value=original_msg,inline=False)
    resp.add_field(name='Detected Language', value=detected_lang.upper() + country_code_to_emoji_flags[detected_lang], inline=False)
    resp.add_field(name='Requested By', value=user, inline=False)
    icon = discord.File("translate.jpeg", filename="translate.jpeg")
    resp.set_author(name='Translation', icon_url="attachment://translate.jpeg")
    return resp, icon
def send_translation_request(message, target):
    url = api_url
    data = {
        "q": message,
        "source": "auto",
        "target": target,
        "format": "html"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

if __name__ == '__main__':
    run()