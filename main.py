import os
import discord
import requests
import json
from discord import Embed

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
api_url = "https://libretranslate.eownerdead.dedyn.io/translate"
emoji_flag_to_country_code = {
    "🇩🇪": "de",  # German flag
    "🇺🇸": "en",  # United States flag
    "🇬🇧": "en",  # United Kingdom flag
    "🇫🇷": "fr",  # French flag
    "🇮🇹": "it",  # Italian flag
    "🇨🇳": "cn",  # China
    "🇮🇳": "in",  # India
    "🇮🇩": "id",  # Indonesia
    "🇵🇰": "pk",  # Pakistan
    "🇧🇷": "br",  # Brazil
    "🇳🇬": "ng",  # Nigeria
    "🇧🇩": "bd",  # Bangladesh
    "🇷🇺": "ru",  # Russia
    "🇯🇵": "jp",  # Japan
    "🇲🇽": "mx",  # Mexico
    "🇵🇭": "ph",  # Philippines
    "🇪🇬": "eg",  # Egypt
    "🇪🇹": "et",  # Ethiopia
    "🇻🇳": "vn",  # Vietnam
    "🇨🇩": "cd",  # Democratic Republic of the Congo
    "🇹🇷": "tr",  # Turkey
    "🇮🇷": "ir",  # Iran
    "🇹🇭": "th",  # Thailand
}
environment = {'pw': ""}
verified_servers = []

def run():
    print("running client...")
    token = os.getenv('TOKEN')
    environment['pw'] = os.getenv('PASSWORD')
    client.run(token)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$Login"):
        k = message.content.split("Login ", 1)[1]
        if k == environment['pw']:
            server_id = message.guild.id
            verified_servers.append(server_id)

@client.event
async def on_reaction_add(reaction, user):
    server_id = reaction.message.guild.id
    if not server_id in verified_servers:
        reaction.message.channel.send(content="Please log in.")
        return
    if reaction.emoji in emoji_flag_to_country_code:
        target_lang = emoji_flag_to_country_code[reaction.emoji]
        message = reaction.message.content
        response = send_translation_request(message, target_lang)
        detected_language = response['detectedLanguage']['language']
        translation = response['translatedText']
        embedding = create_embedding(message, translation, detected_language, user.name)
        await reaction.message.channel.send(embed=embedding)

def create_embedding(original_msg, translation, detected_lang, user):
    resp = Embed(title='Translation', description=translation, color=0x00ff00)
    resp.add_field(name='original message', value=original_msg,inline=False)
    resp.add_field(name='detected language', value=detected_lang.capitalize(), inline=False)
    resp.add_field(name='requested by', value=user, inline=False)
    return resp
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