from Command import Command


class CmdMySettings(Command):

    def __init__(self, users):
        Command.__init__(self, users)
        self.SETTINGS = {
            "help": lambda user, value: self.help(),
            "score_emoji": lambda user, value: self.set_score_emoji(user, value),
        }

    def process(self):
        user = self.get_sending_user()
        if user is None:
            self.answer('CmdMySettings.process(): user is None, this is weird!')
        else:
            if not self.has_text():
                self.answer('🤦🏽 Do not edit commands!')
            else:
                str_args = self.update.message.text.split()
                if len(str_args) < 3:
                    self.help()
                else:
                    setting = str_args[1].lower()
                    value = [arg.lower() for arg in str_args[2:]]
                    if self.SETTINGS[setting](user, value):
                        self.answer('✔️')
                    else:
                        self.answer('This did not work!')

    def set_score_emoji(self, user, value):
        if len(value) > 1:
            return user.set_score_emoji(value[0], value[1])
        else:
            return False

    def help(self):
        self.answer('Available settings:\n'
                    '    - score_emoji: set the emoji that the bot shows when you receive points\n'
                    '        usage: /my_settings score_emoji <amount> <emoji>\n'
                    '        example: /my_settings score_emoji +1 🤦🏽')
