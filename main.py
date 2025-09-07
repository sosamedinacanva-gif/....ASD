import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Variables de entorno
SESSION = os.getenv("TELETHON_SESSION")
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
FROM_CHANNEL = os.getenv("TELEGRAM_FROM_CHANNEL")  # sin @
TO_CHAT_ID = int(os.getenv("TELEGRAM_TO_CHAT_ID"))  # ej: -1001234567890

# Ruta del archivo contador
COUNTER_FILE = "counter.txt"

# Inicia cliente de Telegram
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# Obtiene el siguiente número del contador
def get_next_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return 1
    with open(COUNTER_FILE, "r") as f:
        count = int(f.read().strip())
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count + 1))
    return count

@client.on(events.NewMessage(chats=FROM_CHANNEL))
async def handler(event):
    msg = event.message

    # Verifica si el mensaje contiene un archivo/documento
    if msg.file:
        try:
            # Extraer extensión del archivo original
            original_ext = msg.file.name.split(".")[-1] if msg.file.name and "." in msg.file.name else "bin"
            count = get_next_count()
            new_filename = f"xkorly_{count}.{original_ext}"

            # Descargar el archivo y renombrarlo
            path = await msg.download_media(file=new_filename)

            # Enviar el archivo con nuevo nombre y sin texto adicional
            await client.send_file(
                TO_CHAT_ID,
                file=path,
                caption=f"Archivo: {new_filename}"
            )

            print(f"📦 Enviado como {new_filename}")

            # Eliminar archivo local después de enviar
            os.remove(path)

        except Exception as e:
            print(f"❌ Error al reenviar archivo: {e}")
    else:
        print("⏭️ No es un archivo. Ignorado.")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🤖 Bot conectado como: {me.username or me.first_name}")
    print(f"📡 Escuchando mensajes del canal: {FROM_CHANNEL}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
