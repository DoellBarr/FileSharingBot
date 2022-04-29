from datetime import datetime as dt
from bot import Client
from pyrogram import filters
from pyrogram.types import Message


@Client.on_message(filters.command("ping"))
async def ping_(c: Client, m: Message):
    x = await m.reply("Ping....")
    ping = round((dt.now() - m.date).microseconds / int(1e6), 2)
    await x.edit(
        f"""Pong!
Pyrogram Latency: {ping}ms"""
    )
