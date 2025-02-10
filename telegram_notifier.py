import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from telegram.helpers import escape_markdown
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        config = Config()
        token = config.get('telegram.token')
        chat_id = config.get('telegram.chat_id')
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, message):
        try:
            # escaped_message = escape_markdown(message, version=2)
            sent_message = await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="HTML")
            logger.info(f"Message sent to Telegram chat {self.chat_id}: {message}")
        except TelegramError as e:
            logger.error(f"Failed to send message to Telegram: {e}")

# Example usage
if __name__ == "__main__":
    notifier = TelegramNotifier()
    asyncio.run(notifier.send_message("Hello from <b>Meshtastic Monitor</b>!"))