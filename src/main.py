from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sys
import time
import logging
import os
from datetime import datetime

from BotUsers import BotUsers
from CmdAddAlias import CmdAddAlias
from CmdAddMe import CmdAddMe
from CmdMySettings import CmdMySettings
from CmdReport import CmdReport
from CmdScoreboard import CmdScoreboard
from CmdScore import CmdScore
from CmdShow import CmdShow
from CmdShowAliases import CmdShowAliases
from CmdShowReports import CmdShowReports

# set this logging or the bot will fail silently
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def print_help(update, context):  # list all available cmds
    msg = 'The available commands are:'
    for string in commands.keys():
        msg += u'\n    \U0001F539/' + string
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

bot_users = BotUsers()
users = bot_users.users
cmd_add_me = CmdAddMe(users)
cmd_add_alias = CmdAddAlias(users)
cmd_my_settings = CmdMySettings(users)
cmd_report = CmdReport(users)
cmd_show = CmdShow(users)
cmd_show_aliases = CmdShowAliases(users)
cmd_show_reports = CmdShowReports(users)
cmd_scoreboard = CmdScoreboard(users)

cmd_score = CmdScore(users)  # this should not be added to the other commands, because it is invoked by text msgs

commands = {
    'help': print_help,
    'add_me': cmd_add_me.call,
    'add_alias': cmd_add_alias.call,
    'my_settings': cmd_my_settings.call,
    'report': cmd_report.call,
    'scoreboard': cmd_scoreboard.call,
    'show': cmd_show.call,
    'show_aliases': cmd_show_aliases.call,
    'show_reports': cmd_show_reports.call,
}


def manipulate_score(update, context):
    cmd_score.call(update, context)


def parse_msg(update, context):  # TODO: advanced message parsing => probably via regex
    if hasattr(update.message, 'text'):
        text = update.message.text
        # manipulate score
        if (text[0] == '+' or text[0] == '-') and text[1].isdigit():
            cmd_score.call(update, context)


def maintenance():
    bot_users.save(os.path.join(save_path, 'save'))
    bot_users.check_replenish_score_allotment()


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
dispatcher.add_handler(MessageHandler(Filters.command, print_help))

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
