from telethon import TelegramClient, events
import os
import asyncio
import re

# === CONFIGURACIÓN: DATOS QUE TÚ MISMO DISTE ===
api_id = 25342015
api_hash = 'b047182edee6dd6d9a6ac6989984f46a'
phone = '+18092046403'

from_channel = 'LiveTraffic_channel'
to_chat_username = '@PCGOODMULTIXKO'

# === NOMBRE DEL ARCHIVO DE CONTADOR ===
counter_file = 'counter.txt'

# === FUNCIONES ===
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

client = TelegramClient('session', api_id, api_hash)

async def main():
    await client.start(phone=phone)
    me = await client.get_me()
    print(f"🤖 Bot conectado como: {me.first_name}")

    from_entity = await client.get_entity(from_channel)
    to_entity = await client.get_entity(to_chat_username)

    @client.on(events.NewMessage(chats=from_entity))
    async def handler(event):
        if event.file:
            try:
                # Crear nombre único como xkorly_1.zip, xkorly_2.zip, etc.
                count = get_counter()
                extension = event.file.ext or ".zip"
                new_filename = f"xkorly_{count}{extension}"

                # Reenviar archivo sin texto ni publicidad
                await client.send_file(
                    to_entity,
                    event.file,
                    caption="",  # Sin texto
                    force_document=True,
                    file_name=new_filename
                )

                print(f"✅ Archivo reenviado como {new_filename}")
                increment_counter()

            except Exception as e:
                print("❌ Error al reenviar archivo:", e)
        else:
            print("⚠️ Mensaje sin archivo, ignorado.")

    print(f"📡 Escuchando mensajes del canal: {from_channel}")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
