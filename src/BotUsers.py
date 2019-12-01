import BotUser
import json
from os import listdir
from os.path import isfile, join
from sys import maxsize

# constants | TODO: maybe put this in some kind of cfg file
MAX_ALIAS_LENGTH = 256

class BotUsers:

    def __init__(self):
        self.list = []

    def add_user(self, update, context):
        id_ = update.effective_user.id
        name_ = update.effective_user.first_name

        # find out whether the user already exists
        is_new_user = "true"
        for user in self.list:
            if id_ == user.id_nr:
                is_new_user = False
                break

        # accordingly add it or don't
        if is_new_user:
            self.list.append(BotUser.BotUser(id_, name_))
            output = "added user: " + name_;
        else:
            output = "I already made your acquaintance " + name_ + "."

        context.bot.send_message(chat_id=update.effective_chat.id, text=output)

    def add_alias(self, update, context):
        # check for comma delimited arguments, this has precedence
        comma_args = update.message.text.split(',')
        if len(comma_args) >= 3:  # if input is valid and comma separated
            user_name = comma_args[1].lower()
            new_alias = comma_args[2].lower()
        else:
            args = update.message.text.split(' ',2)
            if len(args) >= 3:  # if space separation is valid
                user_name = args[1].lower()
                new_alias = args[2].lower()
            else:  # invalid input -> send notification and abort
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='invalid input format, it needs to be like this:\n'
                                              ' \\add_alias,<current_name>,<new_alias>\n'
                                              '  example: \\add_alias,Peter,MC Brigitte')
                return
        # arguments have correct form, now the important stuff:
        alias_len = len(new_alias)
        if alias_len < MAX_ALIAS_LENGTH:  # aliases should not exceed max length
            user = self.get_user(user_name)
            if user:
                if user.add_alias(new_alias):
                    output = f'{user.name} is now also called {new_alias}'
                else:
                    output = f'Could not set new alias \'{new_alias}\''
            else:
                output = f'could not find user named {user_name}!'
        else:
            output = f'aliases may only be {MAX_ALIAS_LENGTH} characters long, yours was {alias_len}'
        context.bot.send_message(chat_id=update.effective_chat.id, text=output)

    def scoreboard(self, update, context):
        sorted_users = sorted(self.list, key=lambda user: user.score, reverse=True)  # sort list of user objs by score
        output = "Scoreboard:\n"
        idx = 0

        # "same score case": sometimes multiple users will have the same score and should therefore be placed evenly
        next_index_step = 1  # remembers additional index points in "same score case"
        last_score = maxsize  # last users score needs to be kept to detect "same score case"

        for user in sorted_users:
            # index management:
            if user.score < last_score:  # no "same score case"
                idx += next_index_step
                next_index_step = 1
            else:  # "same score case"
                next_index_step += 1  # remember that one place needs to be skipped
            last_score = user.score

            output += f'{idx}. {user.name}: {user.score}\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=output)

    def save(self, path):
        for user in self.list:
            u_path = path + "_" + str(user.id_nr) + ".json"  # make own file for every user
            with open(u_path, 'w') as f:
                json.dump(user.serialize(), f)

    def load(self, path):
        for file_name in listdir(path):
            file_path = join(path, file_name)
            if isfile(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.list.append(BotUser.BotUser.deserialize(data))

    def get_user(self, user_name):
        '''find the user of the given name in the users list and return it,
        if it does not exist delete return false'''
        for user in self.list:
            aliases = user.aliases
            names = [user.name.lower(), ] + aliases
            for name in names:
                if user_name.lower() == name.lower():
                    return user
        return False
