from abc import ABC, abstractmethod


class ReportField:
    def __init__(self):
        pass

    @abstractmethod
    def create_report(self):
        pass


class Report:
    def __init__(self, reporter_id, reason, settlement=None):
        self.reporter_id = reporter_id
        self.reason = reason
        self.settlement = settlement

    @abstractmethod
    def consider(self, settlement, admin_id):
        pass


