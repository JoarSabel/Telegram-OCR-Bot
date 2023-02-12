# Pyhton text extractor

---

This is a simple telegram bot that extracts text from images using PyTessaract.
Usecases: For example if you have a scanned document/book page that contains code that you dont want to bother typing

## Usage

The bot is on telegram (might be down, depending on where/if I host it) @GivesTextFromImageBot
- `/start` to start the bot
- `/help` for help
- `/convert` as a caption on an image with a light backgroud and black text -> gives the text in the image (with some margin of error)
- `/convert_dark` as a caption on an image with a dark background with some mad polychromatic mess of letters -> gives the text in the image (with some margin of error)

## Other

Requires PyTessaract installed on hostmachine if you aim to run it without docker-compose
