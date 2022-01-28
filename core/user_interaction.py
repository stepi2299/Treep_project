from .reports import ReportField
from datetime import datetime
from abc import abstractmethod, ABC
import pytz


class UserInteraction(ReportField):
    def __init__(self, text):
        self.text = text
        self.creation_date = datetime.now(pytz.utc)

    @abstractmethod
    def create_report(self, reporter_id, reason):
        pass
