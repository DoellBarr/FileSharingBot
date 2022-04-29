from bot import Client
from pyrogram import filters
from pyrogram.types import Message


@Client.on_message(filters.command("help"))
async def help_(_, m: Message):
    return await m.reply("Tanyakan kepada @shohih_abdul")
