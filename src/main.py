from asyncio.queues import Queue
import logging
from typing import NoReturn
from PIL import Image
from pytesseract import pytesseract
from telegram import Bot, Message
import asyncio
import os

def processImage(image_path: str) -> str:
    
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    print(text[:-1])
    return text



# Bot stuff
from telegram import __version__ as TG_VER


try:

    from telegram import __version_info__

except ImportError:

    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]


if __version_info__ < (20, 0, 0, "alpha", 1):

    raise RuntimeError(

        f"This example is not compatible with your current PTB version {TG_VER}. To view the "

        f"{TG_VER} version of this example, "

        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"

    )

from telegram import Bot

from telegram.error import Forbidden, NetworkError


logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

logger = logging.getLogger(__name__)



async def main() -> NoReturn:

    """Run the bot."""

    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    async with Bot(BOT_TOKEN) as bot:

        # get the first pending update_id, this is so we can skip over it in case

        # we get a "Forbidden" exception.

        try:

            update_id = (await bot.get_updates())[0].update_id

        except IndexError as e:
            logger.info('Got IndexError with the following message %s', e)
            update_id = None


        logger.info("listening for new messages... %s", update_id)

        while True:

            try:

                update_id = await handleImage(bot, update_id)
                #print('bob')

            except NetworkError:

                await asyncio.sleep(1)

            except Forbidden:

                # The user has removed or blocked the bot.
                if update_id:
                    update_id = update_id + 1

async def handleImage(bot: Bot, update_id: int) -> int:
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1


        if update.message:
            if update.message.document and update.message.document.mime_type.__eq__('image/png'):
                logger.info('Handling image...')
                file_id = update.message.document.file_id
                new_file = await bot.get_file(file_id)
                await new_file.download_to_drive(custom_path='assets/image_to_process.png')
            
                result = processImage(r'assets/image_to_process.png')
                logger.info('Got this: %s', result)
                await update.message.reply_text(result)
            else: 
                await update.message.reply_text('beep boop, I am a bot designed for OCR tasks only')
        return next_update_id
    return update_id
            

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
