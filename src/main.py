from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sys
import time
import logging
import os
from datetime import datetime

from BotUsers import BotUsers
from CmdAddMe import CmdAddMe
from CmdShowReports import CmdShowReports
from CmdMySettings import CmdMySettings
from CmdAddAlias import CmdAddAlias
from CmdShowAliases import CmdShowAliases
from CmdReport import CmdReport
from CmdScoreboard import CmdScoreboard
from Command import Command

# set this logging or the bot will fail silently
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def print_help(update, context):  # list all available cmds
    msg = 'The available commands are:'
    for string in commands.keys():
        msg += u'\n    \U0001F539/' + string
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def manipulate_score(update, context):
    text = update.message.text
    input_name = text.split(None, 2)[1]
    input_amount = int(text.split(None, 1)[0])
    amount = max(min(input_amount, 2), -1)  # cut score to be within [-1,2]

    cmd = Command(users)  # TODO: this is really ugly! -> maybe move get_user back to BotUsers class
    user = cmd.get_user(input_name)
    if user is not None:
        if user.id_nr == update.effective_user.id and amount != 0:  # manipulation of own score is not allowed
            output = u'Nice try, noob!'
        else:  # normal case
            user.manipulate_score(amount)
            # output = input_name + u' received ' + str(amount) + u' pts and therefore has a score of ' + str(user.score)
            amount_str = str(amount)
            if amount >= 0:
                amount_str = '+' + amount_str
            output = f'💁 {user.emoji_set[amount_str]}'
    else:  # user does not exist
        output = u'I\'ve never heard of this "' + input_name + u'"'
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


bot_users = BotUsers()
users = bot_users.users
cmd_add_me = CmdAddMe(users)
cmd_add_alias = CmdAddAlias(users)
cmd_my_settings = CmdMySettings(users)
cmd_report = CmdReport(users)
cmd_show_aliases = CmdShowAliases(users)
cmd_show_reports = CmdShowReports(users)
cmd_scoreboard = CmdScoreboard(users)

commands = {
    'help': print_help,
    'add_me': cmd_add_me.call,
    'add_alias': cmd_add_alias.call,
    'my_settings': cmd_my_settings.call,
    'report': cmd_report.call,
    'scoreboard': cmd_scoreboard.call,
    'show_aliases': cmd_show_aliases.call,
    'show_reports': cmd_show_reports.call,
}


def parse_msg(update, context):  # TODO: advanced message parsing => probably via regex
    if hasattr(update.message, 'text'):
        text = update.message.text
        # manipulate score
        if (text[0] == '+' or text[0] == '-') and text[1].isdigit():
            manipulate_score(update, context)


def maintenance():
    bot_users.save(os.path.join(save_path, 'save'))


def handle_text(update, context):
    if not hasattr(update.message, 'text'):
        print(f'{datetime.now().isoformat()} received message without text (maybe edit) \tfrom: {update.effective_user.id}')
    print(f'{datetime.now().isoformat()} received: {update.message.text} \tfrom: {update.effective_user.id}')
    sys.stdout.flush()
    parse_msg(update, context)


# def main():
# load data
gcw = os.getcwd()
cfg_path = os.path.join(gcw, 'cfg')
save_path = os.path.join(gcw, 'saves')
bot_users.load(save_path)

# get token from file and create bot
token_path = sys.argv[1]
with open(token_path, 'r') as f:
    TOKEN = f.read()
    f.close()
TOKEN = TOKEN.split('\n', 1)[0]  # need this line because for some reason a line ending appears on linux

# telegram lib init magic
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# add handlers
dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
for key, function in commands.items():
    dispatcher.add_handler(CommandHandler(key, function))

print('starting event loop')
sys.stdout.flush()
updater.start_polling()

# trigger maintenance (e.g. saving data persistently) every 10s
while 1:
    time.sleep(10)
    maintenance()
    # TODO: commands as subclasses of parent that implements e.g. validity checks (see #1) and arg parsing,
    #  implement __repr__ for all classes
    #  random Beleidigungen,
    #  proper help texts

# if __name__ == '__main__':
#    main()
