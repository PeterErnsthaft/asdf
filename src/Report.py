from datetime import datetime, timedelta
import pytz

TZ = pytz.timezone('Europe/Berlin')
VALID_TIME = timedelta(hours=6)
REPORT_TYPES = {
    'score_spam': {'critical_number': 4, 'penalty': 10},
    'other_abuse': {'critical_number': 7, 'penalty': 20},
}


class Report:

    def __init__(self, issuing_user, reason):
        self.issuing_user = issuing_user
        self.reason = reason
        self.time = datetime.now(tz=TZ)

    def still_valid(self):  # if timed out, returns false
        return datetime.now(tz=TZ) - self.time < VALID_TIME

