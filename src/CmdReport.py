from Command import Command
from Report import Report, REPORT_TYPES


class CmdReport(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        user, rest = self.parse_username_first_arg()  # split by white spaces
        if user is not None and len(rest) >= 1:
            reason = rest[0].lower()
            if reason in REPORT_TYPES:
                # add report
                user.add_report(Report(self.update.effective_user.first_name, reason), self.update, self.context)
            else:
                self.answer(f'invalid user or reason! valid reasons are: {REPORT_TYPES.keys()}')
        else:  # invalid input -> send notification and abort
            self.answer('invalid input, it needs to be like this:\n'
                        ' /report <user_name> <reason>\n'
                        '  example: /report Peter other_abuse')

