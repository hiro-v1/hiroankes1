import asyncio

from antigcast import Bot
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageDeleteForbidden, UserNotParticipant

from antigcast.config import *
from antigcast.helpers.tools import *
from antigcast.helpers.admins import *
from antigcast.helpers.message import *
from antigcast.helpers.database import *


@Bot.on_message(filters.command("addbl") & ~filters.private & Admin)
async def addblmessag(app : Bot, message : Message):
    trigger = get_arg(message)
    if message.reply_to_message:
        trigger = message.reply_to_message.text or message.reply_to_message.caption

    xxnx = await message.reply(f"`Menambahakan` {trigger} `ke dalam blacklist..`")
    try:
        await add_bl_word(trigger.lower())
    except BaseException as e:
        return await xxnx.edit(f"Error : `{e}`")

    try:
        await xxnx.edit(f"{trigger} `berhasil di tambahkan ke dalam blacklist..`")
    except:
        await app.send_message(message.chat.id, f"{trigger} `berhasil di tambahkan ke dalam blacklist..`")

    await asyncio.sleep(5)
    await xxnx.delete()
    await message.delete()

@Bot.on_message(filters.command("delbl") & ~filters.private & Admin)
async def deldblmessag(app : Bot, message : Message):
    trigger = get_arg(message)
    if message.reply_to_message:
        trigger = message.reply_to_message.text or message.reply_to_message.caption

    xxnx = await message.reply(f"`Menghapus` {trigger} `ke dalam blacklist..`")
    try:
        await remove_bl_word(trigger.lower())
    except BaseException as e:
        return await xxnx.edit(f"Error : `{e}`")

    try:
        await xxnx.edit(f"{trigger} `berhasil di hapus dari blacklist..`")
    except:
        await app.send_message(message.chat.id, f"{trigger} `berhasil di hapus dari blacklist..`")

    await asyncio.sleep(5)
    await xxnx.delete()
    await message.delete()

@Bot.on_message(filters.command("listbl") & ~filters.private & Admin)
async def daftar_blacklist(app: Bot, message: Message):
    try:
        chat_id = message.chat.id
        bl_words = await get_bl_words(chat_id)
        if not bl_words:
            await message.reply("Tidak ada kata-kata yang di-blacklist.")
            return

        bl_list = "\n".join([f"{idx + 1}. {word}" for idx, word in enumerate(bl_words)])
        response_text = f"<blockquote>**Daftar kata-kata yang di-blacklist di grup ini ({len(bl_words)} kata):**\n{bl_list}</blockquote>"
        await message.reply(response_text)
    except Exception as e:
        await message.reply(f"Error: `{e}`")

@Bot.on_message(filters.text & ~filters.group)
async def deletermessag(app: Bot, message: Message):
    text = f"Maaf, Grup ini tidak terdaftar di dalam list. Silahkan hubungi owner Untuk mendaftarkan Group Anda.\n\n**Bot akan meninggalkan group!**"
    chat = message.chat.id
    chats = await get_actived_chats()
    
    if not await isGcast(filters, app, message):
        if chat not in chats:
            await message.reply(text=text)
            await asyncio.sleep(5)
            try:
                await app.leave_chat(chat)
            except UserNotParticipant as e:
                print(e)
            return
    
    try:
        if await isGcast(filters, app, message):
            await message.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await message.delete()
    except MessageDeleteForbidden:
        pass

@Bot.on_message(filters.text & ~filters.private)
async def cek_blacklist(app: Bot, message: Message):
    chat_id = message.chat.id
    text = message.text.lower() if message.text else ""
    
    # Dapatkan daftar kata yang di-blacklist untuk grup ini
    bl_words = await get_bl_words()
    if not bl_words:
        return
    
    # Periksa apakah pesan mengandung kata yang di-blacklist
    for word in bl_words:
        if word in text:
            try:
                await message.delete()
                return
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.delete()
            except Exception as e:
                print(e)
                return
