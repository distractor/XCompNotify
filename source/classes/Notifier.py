import logging
import os

import telegram


class Notifier:
    def __init__(self):
        logging.info("Notifier initializing.")
        try:
            self.chat_id = os.environ.get("CHAT_ID")
            self.bot = telegram.Bot(os.environ.get("BOT_TOKEN"))
            self.write_timeout = int(os.environ.get("TELEGRAM_WRITE_TIMEOUT"))
        except KeyError as e:
            logging.critical("Missing chat_id or bot_token. Error: '{}'.".format(e))

    async def send_message(self, message):
        """
        Send message to Telegram chat.

        Args:
            message (string): Message.
        """
        logging.debug("Sending message: '{}'.".format(message))
        async with self.bot:
            await self.bot.send_message(text=message, chat_id=self.chat_id, parse_mode="markdown",
                                        write_timeout=self.write_timeout)
        logging.debug("Message sent.")

        return None
