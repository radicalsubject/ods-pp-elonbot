from telegram import (Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (CallbackContext, ConversationHandler)
import os, logging
from modules import pytesseractModule, twitterScreenshotRecognizer
from token_extractor import token
print(token)
logging.info(f"{token}")
bot = Bot(token)

# # Define a few command handlers. These usually take the two arguments update and
# # context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    user_info = update.message.from_user
    chat_id = update.message.chat.id
    logging.info("Test log! user data read successfully.")
    update.message.reply_text(
"""Привет, {}! 👩🏻‍💻 """.format(user_info.first_name))

    context.chat_data.clear()
    user_data = context.user_data
    user_data.clear()
    return -1

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def test(update, context):
    text = pytesseractModule.read_image()
    update.message.reply_text(f'{text}')

def image_handler(update: Update, context: CallbackContext):
    file_id = update.message.photo[-1].file_id
    file_ = bot.getFile(file_id)
    path = os.getcwd() + "/tmp/" + file_id + ".jpg"
    file_.download(path)
    blacklist = ["bitcoin", "elon", "musk", "crypto", "cryptocurrency", "btc", "eth"]
    response = twitterScreenshotRecognizer.inspect(path)
    
    if response == "tweets":
        text = pytesseractModule.read_image(path)
        if any([(word in text.lower()) for word in blacklist]):
            update.message.reply_text(f'Спамер обноружен! Это похоже на скриншот твиттера c мошенниками. Хватит спамить! 🙄')
            try:
                bot.delete_message(chat_id=update.message.chat_id,
                message_id=update.message.message_id)
            except:
                update.message.reply_text("Can't delete message cause probably i dont have admin rights.")
        else:
            update.message.reply_text(f'Это похоже на скриншот твиттера. U\'re on thin freaking ice!')
    else: 
        update.message.reply_text("Nice pic u got there, be sure not to post twitter screenshoots with Elon Musk on my watch 👀")