from telethon import TelegramClient, events
import os

# ✅ DATOS DE AUTENTICACIÓN
api_id = 25342015
api_hash = 'b047182edee6dd6d9a6ac6989984f46a'
phone = '+18092046403'

# ✅ DATOS DE LOS CHATS
from_channel = 'LiveTraffic_channel'  # canal origen
to_chat_id = -1003004655869           # grupo destino

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

# ✅ INICIAR CLIENTE
client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=from_channel))
async def handler(event):
    if event.file:
        try:
            # Contador y nombre nuevo
            count = get_counter()
            extension = os.path.splitext(event.file.name or '.zip')[-1]
            new_filename = f"xkorly_{count}{extension}"

            # Descargar archivo
            downloaded_path = await event.download_media(file=new_filename)

            # Reenviar archivo con nombre modificado, sin texto
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
    print(f"🤖 Bot conectado como: {(await client.get_me()).first_name}")
    print(f"📡 Escuchando mensajes del canal: {from_channel}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
