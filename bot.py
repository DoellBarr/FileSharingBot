import asyncio
import sys
from base64 import urlsafe_b64decode, urlsafe_b64encode
from configs import fsubs_dict, logger, config, btn
from pyrogram import Client as RawClient, errors, idle, types
from typing import Union, Optional


class Client(RawClient):
    def __init__(self, bot_token: Optional[str] = None):
        super().__init__(
            name="bot",
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=bot_token,
            plugins={"root": "plugins"},
            in_memory=True
        )
        self.btn: list = []
        self.first_name: str = ""
        self.me = None
        self.db: types.Chat = None  # noqa
        self.logger = logger
        self.b64 = urlsafe_b64encode
        self.b64d = urlsafe_b64decode

    async def start(self):
        self.logger(__name__).info("Starting Bot...")
        await super().start()
        self.me = await self.get_me()
        self.first_name = self.me.first_name
        keyboard = []
        temp = []
        for category, link in fsubs_dict.items():
            category = category.capitalize().replace("_", " ")
            try:
                chat = await self.get_chat(link)
            except errors.ChatAdminRequired:
                logger(__name__).error(f"{self.first_name} haruslah menjadi admin di grup {link}")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                sys.exit("Bot dimatikan.")
            except errors.UsernameInvalid:
                logger(__name__).error(f"Link: {link} yang diberikan untuk {category} salah!")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                sys.exit("Bot dimatikan.")
            except errors.UserNotParticipant:
                logger(__name__).error(f"Bot {self.first_name} haruslah menjadi admin di {category}")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                sys.exit("Bot dimatikan.")
            await asyncio.sleep(1)
            try:
                member = await self.get_chat_member(chat.id, self.me.id)
            except errors.UserNotParticipant:
                logger(__name__).error(f"Bot {self.first_name} haruslah menjadi admin di {category}")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                sys.exit("Bot dimatikan.")
            await asyncio.sleep(1)
            invite_link = await chat.export_invite_link()
            if member.status.ADMINISTRATOR:
                keyboard.append(btn(category, url=invite_link))
            else:
                logger(__name__).error(f"{self.first_name} harus menjadi admin di {chat.title}")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                logger(__name__).info("Bot Dimatikan.")
                await self.stop()
        new_keyboard = []
        for i, board in enumerate(keyboard, start=1):
            temp.append(board)
            if i % 3 == 0:
                new_keyboard.append(temp)
                temp = []
            if i == len(keyboard):
                new_keyboard.append(temp)
        self.btn = new_keyboard
        if not config.db_channel:
            logger(__name__).error("Channel database tidak ditemukan!")
            logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
            sys.exit("Bot dimatikan.")
        try:
            self.db = await self.get_chat(config.db_channel)
        except errors.ChatAdminRequired:
            logger(__name__).error(f"{self.first_name} haruslah menjadi admin di grup {config.db_channel}")
            logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
            sys.exit("Bot dimatikan.")
        except errors.UsernameInvalid:
            logger(__name__).error(f"Link: {config.db_channel} yang diberikan untuk channel db salah!")
            logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
            sys.exit("Bot dimatikan.")
        self.logger(__name__).info("Bot berhasil dijalankan!")
        self.logger(__name__).info(
            "Berhasil dijalankan!\nJika butuh bantuan silakan tanya kepada @shohih_abdul"
        )
        await self.idle()

    async def stop(self, *args):
        logger(__name__).info("Bot dihentikan...")
        await super().stop()

    @staticmethod
    async def idle():
        logger(__name__).info("Idling...")
        return await idle()

    if config.logger_group_id:
        async def send_logger(self, message: str):
            try:
                return await self.send_message(config.logger_group_id, message)
            except errors.UserNotParticipant:
                logger(__name__).error(f"{self.first_name} haruslah berada di grup {config.logger_group_id}")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                sys.exit("Bot dimatikan.")
            except errors.ChannelInvalid:
                logger(__name__).error(f"Grup dengan id {config.logger_group_id} tidak ditemukan!\nPastikan id grup yang diberikan benar!")
                logger(__name__).info("Silakan tanyakan kepada @shohih_abdul jika anda membutuhkan bantuan")
                sys.exit("Bot dimatikan.")


bot = Client(config.bot_token)
