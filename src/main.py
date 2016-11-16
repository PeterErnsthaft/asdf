import telepot
import sys
import time
import User
import Users
from pprint import pprint

#users = [User.User(0123, "Eduardo"), User.User(0123, "Edik")]
users = Users.Users()




def print_help(msg): #TODO: list available cmds
    help_out = u'help placeholder'
    bot.sendMessage(msg['chat']['id'], help_out)


def unknown_cmd(msg):
    help_out = u'Unknown command: "' + msg['text'] + u'"'
    bot.sendMessage(msg['chat']['id'], help_out)


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


def parse(msg):
    text = msg['text']
    options = {
        'help': print_help,
        'add_me': bot.sendMessage(msg['chat']['id'], users.add_user(msg)),
    }
    if text[0] == '/':
        options.get(text[1:],unknown_cmd)(msg)

    if (text[0] == '+' or text[0] == '-') and text[1].isdigit():
        manipulate_score(msg)

    pprint(msg)

    for u in users.list:
        u.print_user()
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


