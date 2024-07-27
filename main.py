import os
import discord
import requests
from dotenv import load_dotenv
import json
from discord import Embed

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
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
    print("Loading environment variables...")
    load_dotenv()
    token = os.getenv('TOKEN')
    environment['pw'] = os.getenv('PW')
    global api_url
    api_url = os.getenv('TRANSLATE_URL')

    if not token:
        print("Error: TOKEN is not set in the environment variables.")
        return
    if not environment['pw']:
        environment['pw'] = ""
        print("Warning: No Password was set")
    if not api_url:
        print("Error: TRANSLATE_URL is not set in the environment variables.")
        return

    print("Running client...")
    client.run(token)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$Login") and message.guild.id not in verified_servers:
        success = login(message)
        if success:
            await message.channel.send(content="Successfully logged in.")
            print(f"Successfully logged in to server: {message.guild.id}")

@client.event
async def on_reaction_add(reaction, user):
    server_id = reaction.message.guild.id
    if not server_id in verified_servers:
        await reaction.message.channel.send(content="Please log in.")
        print(f"Unverified server: {reaction.message.guild.id}")
        return
    if reaction.emoji in emoji_flag_to_country_code:
        target_lang = emoji_flag_to_country_code[reaction.emoji]
        message = reaction.message.content
        response = send_translation_request(message, target_lang)
        if not response or response == "":
            print("Empty response from translation API")
            return
        detected_language = response['detectedLanguage']['language']
        translation = response['translatedText']
        embedding, icon = create_embedding(message, translation, detected_language, user.name)
        await reaction.message.channel.send(embed=embedding, file=icon)

def create_embedding(original_msg, translation, detected_lang, user):
    resp = Embed(description=translation, color=0x00ff00)
    resp.add_field(name='Original Message', value=original_msg, inline=False)
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
        "format": "html",
        #"alternatives": 2,
        #"api_key": ""
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code != 200:
        print(f"Translation API error: {response.status_code} - {response.text}")
    return response.json() if response and response.status_code == 200 else ""

def login(message):
    k = message.content.split("Login ", 1)
    if len(k) > 1:
        k = k[1]
    else:
        k = ""
    print(f"Login attempt with password: {k}")
    if k == environment['pw']:
        server_id = message.guild.id
        verified_servers.append(server_id)
        print(f"Server {server_id} verified.")
        return True
    print("Login failed.")
    return False

if __name__ == '__main__':
    run()