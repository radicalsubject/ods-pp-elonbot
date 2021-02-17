import logging, os, random, re, requests, sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, MessageFilter
from io import BytesIO
from PIL import Image
from modules import twitterScreenshotRecognizer, pytesseractModule

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook(f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(update, context):
    # Creating a handler-function for /start command 
    update.message.reply_text("Hello from Python!\nPress /random to get random number")

def random_handler(update, context):
    # Creating a handler-function for /random command
    number = random.randint(0, 10)
    update.message.reply_text(f'Random number: {number}')

def image_handler(update, context):
    file = context.bot.get_file(update.message.photo[-1].file_id)
    f =  BytesIO(file.download_as_bytearray())

    image = Image.open(f)

    blacklist = ["bitcoin", "elon", "musk", "crypto", "cryptocurrency", "btc", "eth"]
    response = twitterScreenshotRecognizer.inspect(image)

    if response == "tweets":
        text = pytesseractModule.read_image(image)
        if any([(word in text.lower()) for word in blacklist]):
            text= 'Спамер обноружен! Это похоже на скриншот твиттера c мошенниками. Хватит спамить! 🙄'
            context.bot.send_message(chat_id=update.message.chat_id, text=text)
            try:
                context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            except:
                text = "Can't delete message cause probably i dont have admin rights."
                context.bot.send_message(chat_id=update.message.chat_id, text=text)
        else:
            text = 'Это похоже на скриншот твиттера. U\'re on thin freaking ice!'
            context.bot.send_message(chat_id=update.message.chat_id, text=text)


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("random", random_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    
    run(updater)