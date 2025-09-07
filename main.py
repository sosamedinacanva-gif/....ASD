import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

# Configura tus datos en variables de entorno (más abajo te explico cómo)
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")  # Con código de país, ej "+5211234567890"

# Nombre o @username del canal a escuchar (debe ser público o donde estés)
FROM_CHANNEL = os.getenv("TELEGRAM_FROM_CHANNEL")  # ej: "LiveTraffic_channel" o "https://t.me/LiveTraffic_channel"

# ID o username del grupo destino (donde reenviar los mensajes)
TO_CHAT = os.getenv("TELEGRAM_TO_CHAT_ID")  # ej: -1001234567890 o "mi_grupo_privado"

# Texto que quieres eliminar de los mensajes antes de reenviar
FILTER_TEXT = "Need private and exclusive logs? buy access https://t.me/BuyAccessLiveTraffic_bot"

# Crea cliente userbot
client = TelegramClient(StringSession(), API_ID, API_HASH)

async def main():
    print("Conectando...")

    # Iniciar sesión, pedirá código la primera vez si no hay sesión guardada
    await client.start(phone=PHONE)

    print("Conectado como:", await client.get_me())

    # Intenta unirte al canal si no estás aún
    try:
        await client(JoinChannelRequest(FROM_CHANNEL))
        print(f"Unido al canal {FROM_CHANNEL}")
    except Exception as e:
        print(f"No fue necesario unirse o error: {e}")

    @client.on(events.NewMessage(chats=FROM_CHANNEL))
    async def handler(event):
        text = event.message.message or ""
        # Filtra el texto no deseado
        filtered_text = text.replace(FILTER_TEXT, "").strip()
        if filtered_text:
            print(f"Reenviando mensaje filtrado:\n{filtered_text}\n")
            await client.send_message(TO_CHAT, filtered_text)
        else:
            print("Mensaje filtrado vacío, no se reenvió.")

    print("Bot corriendo, escuchando mensajes...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
