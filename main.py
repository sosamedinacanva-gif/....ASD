import re
import asyncio
from telethon import TelegramClient, events
from flask import Flask

API_ID = 25342015
API_HASH = "b047182edee6dd6d9a6ac6989984f46a"
PHONE = "+18092046403"

FROM_CHANNEL = "LiveTraffic_channel"
TO_CHAT_ID = -1003004655869  # Tu grupo privado

app = Flask(__name__)

def filtrar_mensaje(texto):
    texto_filtrado = re.sub(
        r"Need private and exclusive logs\? buy access https://t\.me/BuyAccessLiveTraffic_bot",
        "",
        texto
    )
    return texto_filtrado.strip()

client = TelegramClient('user_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=FROM_CHANNEL))
async def handler(event):
    texto_original = event.message.message
    texto_limpio = filtrar_mensaje(texto_original)
    if texto_limpio:
        await client.send_message(TO_CHAT_ID, texto_limpio)
        print(f"Reenviado mensaje: {texto_limpio}")

@app.route("/")
def home():
    return "Bot is running!"

async def main():
    await client.start(PHONE)  # Aquí hará login la primera vez
    print("Conectado como usuario, escuchando canal...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()
    asyncio.run(main())
