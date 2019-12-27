from Command import Command
from sys import maxsize


class CmdScoreboard(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        sorted_users = sorted(self.users, key=lambda user: user.score, reverse=True)  # sort list of user objs by score
        output = "Scoreboard:\n"
        idx = 0

        # "same score case": sometimes multiple users will have the same score and should therefore be placed evenly
        next_index_step = 1  # remembers additional index points in "same score case"
        last_score = maxsize  # last users score needs to be kept to detect "same score case"

        for user in sorted_users:
            # index management:
            if user.score < last_score:  # no "same score case"
                idx += next_index_step
                next_index_step = 1
            else:  # "same score case"
                next_index_step += 1  # remember that one place needs to be skipped
            last_score = user.score
            output += f'{idx}. {user.name}: {user.score}\n'
        self.answer(output)
