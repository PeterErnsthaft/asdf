from Report import REPORT_TYPES

class BotUser:

    def __init__(self, id_nr, name, score=0, aliases=[], reports=[]):
        self.id_nr = id_nr
        self.name = name
        self.aliases = aliases
        self.score = score
        self.reports = reports

    def print_user(self): #TODO print whole user data
        print(self.name)

    def manipulate_score(self, amount):
        self.score += amount

    def add_alias(self, alias):
        alias_lower = alias.lower()  # converted to lower case
        self.aliases.append(alias_lower)

    def add_report(self, report, update, context):
        self.reports.append(report)
        self.reports[:] = [r for r in self.reports if r.still_valid()]  # delete reports that are timed out
        self.penalize(update, context)
        # print(f'report added for {self.name}! reason: {report.reason} by {report.issuing_user}')
        # for r in self.reports:
        #     print(f'{r.time}: {r.issuing_user} for {r.reason}')

    # TODO: check if critical number of reports is reached and penalize

    def penalize(self, update, context) :
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
