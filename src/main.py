import telepot
import sys
import time
import User
users = [User.User(0123, "Eduardo", ["Udo", "Edo"]), User.User(0123, "Eduardo", ["Udo", "Edo"])]
score_edo = 0
a = 1


def get_user_id(user_name):
    for user in users:
        if user_name == user:
            return 1
    return -1


def parse(msg):
    for u in users:
        u.print_user()
    text = msg['text']
    if text[0] == '+' and text[1].isdigit():
        user_name = text.split(' ', 2)[1]
        if get_user_id( user_name ) != -1:
            amount = text.split(' ', 1)[0]
            increment = int(amount)
            global score_edo
            score_edo += increment
            bot.sendMessage(msg['chat']['id'], 'es gab ' + amount + u' f\u00fcr ' + user_name + 'Edo hat jetzt ' + str(score_edo))
#  = 'Nein, du bist hier der ' + msg['text'] + ', lieber ' + msg['chat']['first_name']


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        parse(msg)


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)


