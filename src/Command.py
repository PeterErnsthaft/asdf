import BotUser
import json
import jsonpickle
from os import listdir
from os.path import isfile, join
from sys import maxsize

# constants | TODO: maybe put this in some kind of cfg file
MAX_ALIAS_LENGTH = 256


class Command:

    def __init__(self, users):
        self.users = users
        self.update = None
        self.context = None

    # every command is supposed to be called via this function
    def call(self, update, context):
        self.update = update
        self.context = context
        self.process()
        if self.has_text():
            print(f'processed command: {self.update.message.text}; chat id: {self.update.effective_chat.id}')
        else:
            print('received message without text')

    def process(self):
        raise NotImplementedError()  # this method needs to be overridden by specific commands (child classes)

    def get_sending_user(self):
        return self.get_user_by_id(self.update.effective_user.id)

    def has_text(self):
        return hasattr(self.update.message, 'text')

    def parse_username_first_arg(self, delimiter=None):
        if not self.has_text():
            self.answer('🤦🏽 Do not edit commands!')
            return None, None
        else:
            args = self.update.message.text.split(delimiter)
            if len(args) < 2:
                return None, None
            else:
                user_name = args[1].lower()
                user = self.get_user(user_name)
                return user, args[2:]

    def answer(self, text):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=text)

    def get_user(self, user_name):
        '''find the user of the given name in the users list and return it,
        if it does not exist: return None'''
        for user in self.users:
            aliases = user.aliases
            names = [user.name.lower(), ] + aliases
            for name in names:
                if user_name.lower() == name.lower():
                    return user
        return None

    def get_user_by_id(self, id_nr):
        '''find the user of the given id in the users list and return it,
        if it does not exist: return None'''
        for user in self.users:
            if user.id_nr == id_nr:
                return user
        return None

    # def check_validity(update, context):
    #     return hasattr(update.message, 'text')
    #
    # def parse_username_first_arg(update, context):
    #     args = update.message.text.split(None, 2)
    #     if len(args) >= 2:
    #         user_name = args[1].lower()
    #         user = users.get_user(user_name)
    #         return (user, args[2:])
    #
    # def parse_username_first_arg(update, context, answer):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text=answer)