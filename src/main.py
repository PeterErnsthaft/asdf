import telepot
import sys
import time
import BotUser
import BotUsers
import os
from pprint import pprint

#users = [User.User(0123, "Eduardo"), User.User(0123, "Edik")]
users = BotUsers.BotUsers()
TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.Bot(TOKEN)



def print_help(msg):    # TODO: list all available cmds
    help_out = 'The available commands are:'  # pprint(options)
    for string in options.keys():
        help_out += u'\n    \U0001F539/' + string
    return help_out


def unknown_cmd(msg):
    help_out = u'Unknown command: "' + msg['text'] + u'"'
    return help_out


def manipulate_score(msg):
    text = msg['text']
    input_name = text.split(' ', 2)[1]
    input_amount = int(text.split(' ', 1)[0])
    amount = max(min(input_amount, 2), -1)  # cut score to be within [-1,2]

    user = users.get_user(input_name)
    if user.id_nr == msg['from']['id'] and amount != 0:     # manipulation of own score is not allowed...
        output = u'Nice try, noob!'
    elif user:                                              # ... and the user needs to exist...
        user.manipulate_score(amount)
        output = input_name + u' received ' + str(amount) + u' pts and therefore has a score of ' + str(user.score)
    else:                                                   # ...but in case it does not:
        output = u'I\'ve never heard of this "' + input_name
    bot.sendMessage(msg['chat']['id'], output)

options = {
    'help': print_help,
    'add_me': users.add_user,
    'add_alias': users.add_alias,
    }


def parse_cmd(msg):
    text = msg['text']
    if text[0] == '/':
        bot.sendMessage(msg['chat']['id'], options.get(text[1:],unknown_cmd)(msg))

    if (text[0] == '+' or text[0] == '-') and text[1].isdigit():
        manipulate_score(msg)

    pprint(msg)

    for u in users.list:
        u.print_user()


def maintenance():
    users.save(os.path.join(save_path, 'save'))


def load_data(path):  # implement loading users etc
    users.load(path)
    print users


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        parse_cmd(msg)




#def main():
gcw = os.getcwd()   # os.path.dirname(__file__)
cfg_path = os.path.join(gcw, 'cfg')
save_path = os.path.join(gcw, 'saves')
load_data(save_path)
bot.message_loop(handle)
print ('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
    maintenance()


#if __name__ == '__main__':
#    main()




