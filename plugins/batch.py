import json
import random
import string
from pyrogram import filters, types, enums, errors
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as markup
from bot import Client


@Client.on_message(filters.command("batch"))
async def _batch(c: Client, m: types.Message):
    base_link = f"https://t.me/{c.username}?"
    random_string = "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(random.randint(10, 20))
    )
    msg = await m.ask(
        "Teruskan / forward pesan pertama yang anda dapat dari channel database",
        parse_mode=enums.ParseMode.MARKDOWN,
    )
    if msg.forward_from_chat and msg.forward_from_chat.id != c.db.id:
        await m.reply("Pesan yang diteruskan bukanlah dari channel database!")
        return msg
    msgs = await msg.ask(
        "Teruskan / forward pesan terakhir yang anda inginkan dari channel database",
        quote=False,
    )
    if msgs.forward_from_chat and msgs.forward_from_chat.id != c.db.id:
        await msgs.delete()
        await m.reply("Pesan yang diteruskan bukanlah dari channel database!")
        return msgs
    if msg.entities and msg.entities[0].type.URL:
        mentity = msg.text.strip().split("/")
        fmsg_id = int(mentity[-1])
        fmsg_chat_id = mentity[-2]
    else:
        fmsg_id = msg.forward_from_message_id
        fmsg_chat_id = msg.forward_from_chat.id
    if msgs.entities and msgs.entities[0].type.URL:
        mentity = msgs.text
        lmsg_id = int(mentity.split("/")[-1])
    else:
        lmsg_id = msgs.forward_from_message_id
    if (
        (isinstance(fmsg_chat_id, str) and fmsg_chat_id.isdigit())
        and int(f"-100{fmsg_chat_id}") != c.db.id
        or (isinstance(fmsg_chat_id, int))
        and fmsg_chat_id != c.db.id
    ):
        return await m.reply("Pesan yang diberikan bukanlah dari channel database!")
    if (
        isinstance(fmsg_chat_id, str)
        and c.db.username
        and fmsg_chat_id != c.db.username
    ):
        return await m.reply("Pesan yang diberikan bukanlah dari channel database!")
    all_msg_id = list(range(fmsg_id, lmsg_id + 1))
    msg_ids = []
    for i in all_msg_id:
        try:
            p = await c.get_messages(c.db.id, i)
            if not p.empty:
                msg_ids.append(p.id)
        except errors.RPCError as e:
            print(e)
    with open("database.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
    data.append(
        {"chat_id": fmsg_chat_id, "msg_id": all_msg_id, "shorten_link": random_string}
    )
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)
    await m.reply(
        "Get Link",
        reply_markup=markup(
            [[btn("Get Link", url=f"{base_link}start={random_string}")]]
        ),
    )
