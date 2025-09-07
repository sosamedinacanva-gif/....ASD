from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import re

API_ID = 25342015
API_HASH = "b047182edee6dd6d9a6ac6989984f46a"
BOT_TOKEN = "8491690343:AAE3z7ZTtbHbRaHlHsYFBpW3jrF7A8241as"
FROM_CHANNEL = "LiveTraffic_channel"
TO_CHAT_ID = -1003004655869

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def filtrar_mensaje(texto):
    texto_filtrado = re.sub(
        r"Need private and exclusive logs\? buy access https://t\.me/BuyAccessLiveTraffic_bot", 
        "", 
        texto
    )
    return texto_filtrado.strip()

@client.on(events.NewMessage(chats=FROM_CHANNEL))
async def handler(event):
    texto_original = event.message.message
    texto_limpio = filtrar_mensaje(texto_original)

    if texto_limpio:
        await client.send_message(TO_CHAT_ID, texto_limpio)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
print("Bot corriendo...")
client.run_until_disconnected()
