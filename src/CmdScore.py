from Command import Command


class CmdScore(Command):

    def __init__(self, users):
        Command.__init__(self, users)

    def process(self):
        text = self.update.message.text
        input_name = text.split(None, 2)[1]
        desired_amount = int(text.split(None, 1)[0])

        target_user = self.get_user(input_name)
        sending_user = self.get_sending_user()
        if target_user is not None and sending_user is not None:
            if target_user.id_nr == sending_user.id_nr and desired_amount != 0:  # manipulation of own score is not allowed
                self.answer(u'Nice try, noob!')
            else:  # normal case
                legit_amount = sending_user.reduce_allotment_and_or_score(desired_amount)
                if legit_amount is not None:
                    target_user.manipulate_score(legit_amount)
                    # self.answer(input_name + u' received ' + str(desired_amount) + u' pts and therefore has a score of ' + str(target_user.score))
                    amount_str = str(legit_amount)
                    if legit_amount >= 0:
                        amount_str = '+' + amount_str
                    self.answer(f'💁 {target_user.emoji_set[amount_str]}')
                else:
                    self.answer(f'❌ Your score is {sending_user.score} and your allotment is {sending_user.allotment}. ' \
                             f'You cannot give that amount of points... 😟')
        else:  # target_user does not exist
            self.answer(u'I\'ve never heard of this "' + input_name + u'"')
