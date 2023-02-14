import logging
from typing import NoReturn
from PIL import Image, ImageOps, ImageEnhance
from pytesseract import pytesseract
from telegram import Bot,Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os

def processImage(image_path: str) -> str:    
    image = Image.open(image_path)

    # Sharpen 
    enhancer = ImageEnhance.Sharpness(image)
    res = enhancer.enhance(4) 

    # Improve contrast
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(2)

    text = pytesseract.image_to_string(res, config='--psm 6 --oem 1')
    return text

def processDarkImage(image_path: str) -> str:
    image = Image.open(image_path)
    image = ImageOps.invert(image.convert('RGB'))
    
    # Sharpen 
    enhancer = ImageEnhance.Sharpness(image)
    res = enhancer.enhance(4) 

    # Improve contrast
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(2)

    text = pytesseract.image_to_string(res)
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
    await update.message.reply_text("Just send me a screenshot of text with the /convert as a caption, that's all I do")

# When image is sent with 'convert' as caption
async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message:
            if update.message.document and update.message.document.mime_type.__eq__('image/png'):
                logger.info('Handling image...')
                file_id = update.message.document.file_id
                new_file = await context.bot.get_file(file_id)
                await new_file.download_to_drive(custom_path='assets/image_to_process.jpg')
            
                result = processImage(r'assets/image_to_process.jpg')
                logger.info('Got this: %s', result)
                await update.message.reply_text(result)
            else: 
                await update.message.reply_text('Looks like you did not provide an image with that command there bud, what am I supposed to convert? (/help for help)')

# When image is sent with 'convert_dark' as caption, this is for images with a dark background
async def convert_dark_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message:
            if update.message.document and update.message.document.mime_type.__eq__('image/png'):
                logger.info('Handling image...')
                file_id = update.message.document.file_id
                new_file = await context.bot.get_file(file_id)
                await new_file.download_to_drive(custom_path='assets/image_to_process.jpg')
            
                result = processDarkImage(r'assets/image_to_process.jpg')
                logger.info('Got this: %s', result)
                await update.message.reply_text(result)
            else: 
                await update.message.reply_text('Looks like you did not provide an image with that command there bud, what am I supposed to convert? (/help for help)')

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

    application.add_handler(CommandHandler("convert_dark",convert_dark_command))
    application.add_handler(MessageHandler(filters.Document.MimeType('image/png') & filters.CaptionRegex(r'convert_dark'),convert_dark_command))
    
    application.add_handler(CommandHandler("convert",convert_command))
    application.add_handler(MessageHandler(filters.Document.MimeType('image/png') & filters.CaptionRegex(r'convert'),convert_command))

    application.run_polling()
            

if __name__ == "__main__":
    main()

