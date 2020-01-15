import sys
import logging
import time
#import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# set this logging or the bot will fail silently
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        out = 'Nein, du bist hier der ' + msg['text'] + ', lieber ' + msg['chat']['first_name']
        #bot.sendMessage(chat_id, out)


def echo(update, context):
    text = update.message.text
    uid = None
    if hasattr(update.message, 'reply_to_message') and hasattr(update.message.reply_to_message, 'from_user'):
        uid = update.message.reply_to_message.from_user.id
    if uid is not None:
        text += '\n**replied to:**\n' + str(uid)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def caps(update, context):
    text_caps = ' '.join(context.str_args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# get token from file and create bot
token_path = sys.argv[1]
with open(token_path, 'r') as f:
    TOKEN = f.read()
    f.close()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

#caps_handler = CommandHandler('caps', caps)
#dispatcher.add_handler(caps_handler)

print('Listening ...')
updater.start_polling()
