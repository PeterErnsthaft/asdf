 
import sys
import time
#import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        out = 'Nein, du bist hier der ' + msg['text'] + ', lieber ' + msg['chat']['first_name']
        #bot.sendMessage(chat_id, out)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
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
