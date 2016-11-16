import telepot
import sys
import time
import User
from pprint import pprint

users = [User.User(0123, "Eduardo"), User.User(0123, "Edik")]
a = 1


def get_user_id(user_name):
    for user in users:
        names = user.aliases
        names.append(user.name)
        for name in names:
            if user_name == name:
                return user
    return False


def add_user(msg):
    id_ = msg['from']['id']
    name_ = msg['from']['first_name']
    is_new_user = "true"
    for user in users:
        if id_ == user.id_nr:
            is_new_user = False
            break
    if is_new_user:
        users.append(User.User(id_, name_))
        output = "added user: " + name_;
    else:
        output = "I already made your acquaintance " + name_ + "."
    bot.sendMessage(msg['chat']['id'], output)


def print_help(msg): #TODO: list available cmds
    help_out = u'help placeholder'
    bot.sendMessage(msg['chat']['id'], help_out)


def unknown_cmd(msg):
    help_out = u'Unknown command: "' + msg['text'] + u'"'
    bot.sendMessage(msg['chat']['id'], help_out)


def manipulate_score(msg):
    text = msg['text']
    input_name = text.split(' ', 2)[1]
    user = get_user_id(input_name)
    input_amount = int(text.split(' ', 1)[0])
    amount = max(min(input_amount, 2), -1)  # cut score to be within [-1,2]
    if user.id_nr == msg['from']['id'] and amount != 0:
        output = u'Nice try, noob!'
    elif user:
        user.manipulate_score(amount)
        output = input_name + u' received ' + str(amount) + u' pts and therefore has a score of ' + str(user.score)
    else:
        output = u'I\'ve never heard of this "' + input_name
    bot.sendMessage(msg['chat']['id'], output)


def parse(msg):
    text = msg['text']
    options = {
        'help': print_help,
        'add_me': add_user,
    }
    if text[0] == '/':
        options.get(text[1:],unknown_cmd)(msg)

    if (text[0] == '+' or text[0] == '-') and text[1].isdigit():
        manipulate_score(msg)

    pprint(msg)


#   for u in users:
#       u.print_user()
#  = 'Nein, du bist hier der ' + msg['text'] + ', lieber ' + msg['chat']['first_name']


def maintenance(): #implement saving and stuff
    pass


def load_data():  # implement loading users etc
    pass


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        parse(msg)


TOKEN = sys.argv[1]  # get token from command-line

load_data()

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)


