from telethon import TelegramClient, events
import os
from flask import Flask
import threading
import asyncio

# ✅ DATOS DE AUTENTICACIÓN
api_id = 25342015
api_hash = 'b047182edee6dd6d9a6ac6989984f46a'
phone = '+18092046403'

# ✅ DATOS DE LOS CHATS
from_channel = 'LiveTraffic_channel'   # canal origen (sin @)
to_chat_id = -1003004655869            # grupo destino

# ✅ ARCHIVO PARA CONTADOR
counter_file = 'counter.txt'

# 🔢 Funciones para contador
def get_counter():
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as f:
            f.write('1')
        return 1
    with open(counter_file, 'r') as f:
        return int(f.read().strip())

def increment_counter():
    count = get_counter() + 1
    with open(counter_file, 'w') as f:
        f.write(str(count))
    return count

# ✅ FLASK SERVER PARA UPTIMEROBOT
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# ✅ TELEGRAM CLIENT
client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=from_channel))
async def handler(event):
    if event.file:
        try:
            count = get_counter()
            extension = os.path.splitext(event.file.name or '.zip')[-1]
            new_filename = f"xkorly_{count}{extension}"

            # Descargar archivo
            downloaded_path = await event.download_media(file=new_filename)

            # Enviar al grupo con nombre nuevo, sin texto
            await client.send_file(
                to_chat_id,
                downloaded_path,
                caption="",  # sin mensaje
                force_document=True
            )

            print(f"✅ Archivo reenviado como {new_filename}")
            increment_counter()
            os.remove(downloaded_path)

        except Exception as e:
            print("❌ Error al reenviar archivo:", e)
    else:
        print("⚠️ Mensaje sin archivo, ignorado.")

async def main():
    await client.start(phone=phone)
    me = await client.get_me()
    print(f"🤖 Bot conectado como: {me.first_name}")
    print(f"📡 Escuchando mensajes del canal: {from_channel}")
    await client.run_until_disconnected()

# ✅ EJECUTAR FLASK + BOT
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
