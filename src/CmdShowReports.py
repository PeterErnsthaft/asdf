from Command import Command


class CmdShowReports(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        user, rest = self.parse_username_first_arg()  # split by white spaces
        answer = ''
        if user is not None:
            answer = user.get_reports_string()
        else:
            answer = 'invalid input, it needs to be like this:\n' \
                     '\t/show_reports <user_name>\n' \
                     '\texample: /show_reports Peter'
        self.answer(answer)
