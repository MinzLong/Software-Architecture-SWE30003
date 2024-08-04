from bson import ObjectId
from data_access.database import get_database

db = get_database()

class Invoice:
    def __init__(self, booking_id, amount):
        self.booking_id = booking_id
        self.amount = amount

    def create_invoice(self):
        invoice_id = db.invoices.insert_one({
            "booking_id": ObjectId(self.booking_id),
            "amount": self.amount
        }).inserted_id
        return f"Invoice created successfully with ID: {invoice_id}"
