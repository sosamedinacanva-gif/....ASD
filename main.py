import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Carga variables de entorno
SESSION = os.getenv("TELETHON_SESSION")
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
FROM_CHANNEL = os.getenv("TELEGRAM_FROM_CHANNEL")  
TO_CHAT_ID = int(os.getenv("TELEGRAM_TO_CHAT_ID"))  # ej: -1001234567890

# Inicia el cliente
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=FROM_CHANNEL))
async def handler(event):
    msg = event.message

    try:
        # Reenvía TODO el mensaje tal como está
        await msg.forward_to(TO_CHAT_ID)
        print("📦 Mensaje reenviado correctamente.")
    except Exception as e:
        print(f"⚠️ Error al reenviar mensaje: {e}")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🤖 Bot conectado como: {me.username or me.first_name}")
    print(f"📡 Escuchando mensajes de: {FROM_CHANNEL}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
