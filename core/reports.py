from abc import ABC, abstractmethod


class ReportField:

    @abstractmethod
    def create_report(self, reporter_id, reason):
        pass


class Report:
    def __init__(self, reporter_id, reason, settlement_id=1):
        self.reporter_id = reporter_id
        self.reason = reason
        self.settlement_id = settlement_id

    @abstractmethod
    def consider(self, settlement, admin_id):
        pass


