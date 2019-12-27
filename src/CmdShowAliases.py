from Command import Command


class CmdShowAliases(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        user, rest = self.parse_username_first_arg()  # split by white spaces
        if user is None:  # if no argument is given print all user's aliases
            for user in self.users:
                self.__show_aliases(user)
        else:  # only print aliases of user in the argument
            self.__show_aliases(user)

    def __show_aliases(self, user):
        if user is not None:
            output = f'Aliases of user {user.name}: {user.aliases}'
        else:
            output = f'User not found! Use this command like this:\n' \
                     f'\t/show_aliases <user_name>\n' \
                     f'or, if you want to print the aliases of all users, like this:' \
                     f'\t/show_aliases'
        self.answer(output)
