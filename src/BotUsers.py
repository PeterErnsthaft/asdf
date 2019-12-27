import BotUser
import json
import jsonpickle
from os import listdir
from os.path import isfile, join


class BotUsers:

    def __init__(self):
        self.users = []

    def save(self, path):
        for user in self.users:
            u_path = path + "_" + str(user.id_nr) + ".json"  # make own file for every user
            with open(u_path, 'w') as f:
                f.write(jsonpickle.encode(user))

    def load(self, path):
        for file_name in listdir(path):
            file_path = join(path, file_name)
            if isfile(file_path):
                with open(file_path, 'r') as f:
                    json_string = f.read()
                    self.users.append(jsonpickle.decode(json_string))
