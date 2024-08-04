from abc import ABC, abstractmethod

class IPaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class Visa(IPaymentMethod):
    def process_payment(self, amount):
        return f"Processing Visa payment for amount: {amount}"

class Cash(IPaymentMethod):
    def process_payment(self, amount):
        return f"Processing Cash payment for amount: {amount}"
