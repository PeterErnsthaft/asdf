from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sys
import time
import BotUser
import BotUsers
from Report import Report, REPORT_TYPES
import os
from pprint import pprint
import logging

# set this logging or the bot will fail silently
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# users = [User.User(0123, "Eduardo"), User.User(0123, "Edik")]
users = BotUsers.BotUsers()


def print_help(update, context):  # list all available cmds
    msg = 'The available commands are:'
    for string in options.keys():
        msg += u'\n    \U0001F539/' + string
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


# currently effectively dead (got no wildcard filter for each unknown command)
def unknown_cmd(update, context):
    msg = u'Unknown command: "' + update.message.text + u'"'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def manipulate_score(update, context):
    text = update.message.text
    input_name = text.split(' ', 2)[1]
    input_amount = int(text.split(' ', 1)[0])
    amount = max(min(input_amount, 2), -1)  # cut score to be within [-1,2]

    user = users.get_user(input_name)
    if user:
        if user.id_nr == update.effective_user.id and amount != 0:  # manipulation of own score is not allowed
            output = u'Nice try, noob!'
        else:  # normal case
            user.manipulate_score(amount)
            output = input_name + u' received ' + str(amount) + u' pts and therefore has a score of ' + str(user.score)
    else:  # user does not exist
        output = u'I\'ve never heard of this "' + input_name + u'"'
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


def report(update, context):
    # parse args
    args = update.message.text.split(' ', 2)
    if len(args) >= 3:
        user_name = args[1].lower()
        reason = args[2].lower()
        user = users.get_user(user_name)
        if user and reason in REPORT_TYPES:
            # add report
            user.add_report(Report(update.effective_user.first_name, reason), update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'invalid user or reason! valid reasons are: {REPORT_TYPES.keys()}')
    else:  # invalid input -> send notification and abort
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='invalid input, it needs to be like this:\n'
                                      ' /report <user_name> <reason>\n'
                                      '  example: /report Peter other_abuse')


options = {
    'help': print_help,
    'add_me': users.add_user,
    'add_alias': users.add_alias,
    'scoreboard': users.scoreboard,
    'show_aliases': users.show_aliases,
    'report': report,
}

def parse_msg(update, context):  # TODO: advanced message parsing (maybe parse whole message)
    text = update.message.text

    # manipulate score
    if (text[0] == '+' or text[0] == '-') and text[1].isdigit():
        manipulate_score(update,context)

    # debugging
    for u in users.list:
        u.print_user()


def maintenance():
    users.save(os.path.join(save_path, 'save'))


def load_data(path):  # implement loading users etc
    users.load(path)
    print(users)


def handle_text(update, context):
    print(u'received: ' + update.message.text + "\nfrom: " + str(update.effective_user))
    parse_msg(update, context)

# def main():

# initialize
gcw = os.getcwd()
cfg_path = os.path.join(gcw, 'cfg')
save_path = os.path.join(gcw, 'saves')
load_data(save_path)

# get token from file and create bot
token_path = sys.argv[1]
with open(token_path, 'r') as f:
    TOKEN = f.read()
    f.close()
TOKEN = TOKEN.split('\n', 1)[0] # need this line because for some reason a line ending appears on linux

# telegram lib magic
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# add handlers
dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
for key, function in options.items():
    dispatcher.add_handler(CommandHandler(key, function))

print('starting event loop')
updater.start_polling()

# trigger maintenance (e.g. saving data persistently) every 10s
while 1:
    time.sleep(10)
    maintenance()
    # TODO: print reports, random Beleidigungen, proper help texts

# if __name__ == '__main__':
#    main()
