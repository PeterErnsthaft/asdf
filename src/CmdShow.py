from Command import Command
from BotUser import BotUser

class CmdShow(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        if not self.has_text():
            self.answer('🤦🏽 Do not edit commands!')
        else:
            args = self.update.message.text.split()
            user = self.get_sending_user()
            if len(args) < 2:
                self.answer('Invalid command!\n'
                            f'usage: /show <attribute>   - where <attribute> is one of the following {vars(user).keys()}')
            else:
                attribute = args[1].lower()
                if len(args) > 2:
                    user = self.get_user(args[2].lower())
                if hasattr(user, attribute):
                    self.answer(f'{user.name}\'s {attribute}: {getattr(user, attribute)}')
                else:
                    self.answer(f'There is no attribute called \'{attribute}\'')

