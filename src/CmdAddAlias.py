from Command import Command

MAX_ALIAS_LENGTH = 256


class CmdAddAlias(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        # check for comma delimited arguments, this has precedence
        user, rest = self.parse_username_first_arg(delimiter=',')
        if user is None:  # if username was not found when splitting by comma
            user, rest = self.parse_username_first_arg()  # split by white spaces
        if user is not None and rest is not None:
            new_alias = rest[0].lower()
        else:  # invalid input -> send notification and abort
            self.answer('invalid input format, it needs to be like this:\n'
                        ' /add_alias,<current_name>,<new_alias>\n'
                        '  example: /add_alias,Peter,MC Brigitte')
            return
        # arguments have correct form, now the important stuff:
        alias_len = len(new_alias)
        if alias_len < MAX_ALIAS_LENGTH:  # aliases should not exceed max length
            if self.get_user(new_alias) is None:
                user.add_alias(new_alias)
                output = f'{user.name} is now also called {new_alias}'
            else:
                output = f'{user.name} is already known as \'{new_alias}\''
        else:
            output = f'aliases may only be {MAX_ALIAS_LENGTH} characters long, yours was {alias_len}'
        self.answer(output)
