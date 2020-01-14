from datetime import datetime, timedelta
import pytz
from GlobalConstants import TZ

VALID_TIME = timedelta(hours=12)
REPORT_TYPES = {
    'score_spam': {'critical_number': 4, 'penalty': 20},
    'other_abuse': {'critical_number': 4, 'penalty': 30},
}


class Report:

    def __init__(self, issuing_user, reason):
        self.issuing_user = issuing_user
        self.reason = reason
        self.time = datetime.now(tz=TZ)

    def still_valid(self):  # if timed out, returns false
        return datetime.now(tz=TZ) - self.time < VALID_TIME

    def __repr__(self):
        return f'{self.reason} by {self.issuing_user}, time: {self.time.strftime("%Y-%m-%d %H:%M:%S")}'
