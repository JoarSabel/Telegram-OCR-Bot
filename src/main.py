import logging
from typing import NoReturn
from PIL import Image
from pytesseract import pytesseract
from telegram import Bot,Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
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

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

logger = logging.getLogger(__name__)


# When /start is done
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello, I am a bot that turns images of text, into text. Use /help for more info!")

# When /help is called
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Just send me a screenshot of text with the 'convert' as a caption, that's all I do")

# When image is sent with 'convert' as caption
async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.info('We in the convert now!')
        if update.message:
            if update.message.document and update.message.document.mime_type.__eq__('image/png'):
                logger.info('Handling image...')
                file_id = update.message.document.file_id
                new_file = await context.bot.get_file(file_id)
                await new_file.download_to_drive(custom_path='assets/image_to_process.png')
            
                result = processImage(r'assets/image_to_process.png')
                logger.info('Got this: %s', result)
                await update.message.reply_text(result)
            else: 
                await update.message.reply_text('beep boop, I am a bot designed for OCR tasks only')

# When someone inputs some random stuff
async def unkown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('AAAAAUGH I am a bot designed for OCR tasks ONLY (/help for help)')

def main() -> None:

    """Run the bot."""

    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    BOT_TOKEN = os.environ.get('BOT_TOKEN')

    application = Application.builder().bot(Bot(BOT_TOKEN)).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.MimeType('image/png') & filters.CaptionRegex(r'convert'),convert_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unkown))

    application.run_polling()
            

if __name__ == "__main__":
    main()

