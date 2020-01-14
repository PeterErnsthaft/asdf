from emoji import UNICODE_EMOJI

from Report import REPORT_TYPES
from GlobalConstants import SCORE_ALLOTMENT, MIN_AMOUNT, MAX_AMOUNT

MAX_FROM_ALLOTMENT = 2  # maximum number of points that can be spend from the personal allotment

class BotUser:

    def __init__(self, id_nr, name):
        self.id_nr = id_nr
        self.name = name
        self.aliases = []
        self.score = 0
        self.reports = []
        self.allotment = SCORE_ALLOTMENT
        self.emoji_set = {
            '-1': '🤕',
            '+0': '🤖',
            '+1': '🥰',
            '+2': '🤩',
            '+3': '🤴',
            '+4': '🦍',
            '+5': '🔥',
        }

    def print_user(self):  # TODO: implement __repr__
        print(self.name)

    def manipulate_score(self, amount):
        self.score += amount

    def add_alias(self, alias):
        alias_lower = alias.lower()  # converted to lower case
        self.aliases.append(alias_lower)

    def set_score_emoji(self, amount, emoji):
        if amount in self.emoji_set and emoji in UNICODE_EMOJI:
            self.emoji_set[amount] = emoji
            return True
        else:
            return False

    def reduce_allotment_and_or_score(self, desired_amount):
        if self.allotment == 0 and self.score == 0:
            return None
        desired_amount = max(desired_amount, MIN_AMOUNT)  # you cannot give below MIN_AMOUNT points
        desired_amount = min(desired_amount, MAX_AMOUNT)  # you cannot give above MAX_AMOUNT points
        # giving negative points reduces own points:
        if desired_amount < 0:
            amount_from_allotment = 0
            amount_from_score = -desired_amount
        else:
            amount_from_allotment = min(desired_amount, self.allotment,
                                        MAX_FROM_ALLOTMENT)  # give only as much as you can from allotment
            amount_from_score = desired_amount - amount_from_allotment  # give rest from score
        if amount_from_score > self.score:  # check if it is possible
            return None
        else:
            self.allotment -= amount_from_allotment
            self.score -= amount_from_score
            sign = int(desired_amount / abs(desired_amount))
            return (amount_from_allotment + amount_from_score) * sign


    def add_report(self, report, update, context):
        # no need to check whether user has already reported for this reason, penalize only recognized unique user's
        # reports for one type
        self.reports.append(report)
        self.reports[:] = [r for r in self.reports if r.still_valid()]  # delete reports that are timed out
        self.penalize(update, context)
        # print(f'report added for {self.name}! reason: {report.reason} by {report.issuing_user}')

    def get_reports_string(self):
        if self.reports.count == 0:
            return f'No reports for {self.name}!'
        else:
            self.reports.sort(key=lambda report: report.time)
            self.reports.sort(key=lambda report: report.reason)
            res = f'Reports:\n'
            for r in self.reports:
                res += f'\t⚠️ {r}\n'
            return res

    def penalize(self, update, context):
        # count number of users that reported for the same reason
        reports_per_reason = {}
        for report in self.reports:
            if report.reason not in reports_per_reason:  # add new user list for this reason if not existent
                reports_per_reason[report.reason] = []
            if report.issuing_user not in reports_per_reason[report.reason]:  # add issuing user name if not there, yet
                reports_per_reason[report.reason] += [report.issuing_user]

        # penalize if critical number of reports given
        for reason, reporting_users in reports_per_reason.items():
            if len(reporting_users) >= REPORT_TYPES[reason]['critical_number']:
                penalty = REPORT_TYPES[reason]['penalty']
                self.score -= penalty
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'{self.name}, du bist in der Anzeige! {reporting_users} haben dich angezeigt '
                                              f'für {reason}. Die Strafe folgt auf dem Fuße: -{penalty} Punkte')
                # delete all reports the user was just penalized for:
                self.reports[:] = [r for r in self.reports if r.reason != reason]
