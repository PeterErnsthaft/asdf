from Command import Command
from BotUser import BotUser


class CmdAddMe(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        try:
            user_id = self.update.effective_user.id
            name = self.update.effective_user.first_name
        except:
            self.answer("CmdAddMe: invalid input")

        if self.get_user(name) is None:
            self.users.append(BotUser(user_id, name))
            output = "added user: " + name
        else:
            output = "I already made your acquaintance " + name + "."
        self.answer(output)