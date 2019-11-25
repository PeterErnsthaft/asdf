import BotUser
import json
from os import listdir
from os.path import isfile, join


class BotUsers:

    def __init__(self):
        self.list = []

    def add_user(self,msg):
        id_ = msg['from']['id']
        name_ = msg['from']['first_name']

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

        return output

    def add_alias(self,msg):    # TODO: implement
        return "add alias not implemented"

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
            names = user.aliases
            names.append(user.name)
            for name in names:
                if user_name == name:
                    return user
        return False
