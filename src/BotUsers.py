import sys
import json
import jsonpickle
from os import listdir
from os.path import isfile, join
import pytz
from datetime import datetime, timedelta

import BotUser
from GlobalConstants import TZ, SCORE_ALLOTMENT


REPLENISH_PERIOD = timedelta(days=7)
BOT_USERS_ATTRIBUTES_SAVE_FILE = 'bot_users_attributes.json'


class BotUsers:

    def __init__(self):
        self.users = []
        self.attrs = {'last_time_score_replenished': datetime.now()}

    def save(self, path):
        with open(path + "_" + BOT_USERS_ATTRIBUTES_SAVE_FILE, 'w') as f:
            f.write(jsonpickle.encode(self.attrs))
        for user in self.users:
            u_path = path + "_" + str(user.id_nr) + ".json"  # make own file for every user
            with open(u_path, 'w') as f:
                f.write(jsonpickle.encode(user))

    def load(self, path):
        for file_name in listdir(path):
            if file_name[0:5] == 'save_':
                file_path = join(path, file_name)
                if isfile(file_path):
                    with open(file_path, 'r') as f:
                        json_string = f.read()
                        if file_name == "save_" + BOT_USERS_ATTRIBUTES_SAVE_FILE and isfile(file_path):  # load this class' attributes
                            self.attrs = jsonpickle.decode(json_string)
                        else:  # load bot user
                            self.users.append(jsonpickle.decode(json_string))

    def check_replenish_score_allotment(self):
        if datetime.now() > (self.attrs['last_time_score_replenished'] + REPLENISH_PERIOD):
            self.attrs['last_time_score_replenished'] = datetime.now()
            print(f'{self.attrs["last_time_score_replenished"].isoformat()} - replenished score allotments to {SCORE_ALLOTMENT}')
            sys.stdout.flush()
            for user in self.users:
                user.allotment = SCORE_ALLOTMENT
