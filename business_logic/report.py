from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def generate(self):
        pass

class Statistic(Report):
    def generate(self):
        return "Generating statistics report"

class Revenue(Report):
    def generate(self):
        return "Generating revenue report"

class Debt(Report):
    def generate(self):
        return "Generating debt report"

class FactoryReport:
    @staticmethod
    def create_report(report_type):
        if report_type == "1":  # Statistic report
            return Statistic()
        elif report_type == "2":  # Revenue report
            return Revenue()
        elif report_type == "3":  # Debt report
            return Debt()
        else:
            return None
