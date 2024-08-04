import random
import string
from bson import ObjectId
from data_access.database import get_database

db = get_database()

def generate_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class Booking:
    def __init__(self, user_id, parking_slot_id, duration, vehicle, payment_method, amount):
        self.user_id = user_id
        self.parking_slot_id = parking_slot_id
        self.duration = duration
        self.vehicle = vehicle
        self.payment_method = payment_method
        self.amount = amount
        self.short_id = generate_short_id()

    def create_booking(self):
        if not db.parking_slots.find_one({"_id": ObjectId(self.parking_slot_id), "is_occupied": False}):
            return "Parking slot is already occupied!"
        booking_id = db.bookings.insert_one({
            "short_id": self.short_id,
            "user_id": ObjectId(self.user_id),
            "parking_slot_id": ObjectId(self.parking_slot_id),
            "duration": self.duration,
            "vehicle_type": self.vehicle.vehicle_type,
            "license_plate": self.vehicle.license_plate,
            "payment_method": self.payment_method.__class__.__name__,
            "amount": self.amount
        }).inserted_id
        db.parking_slots.update_one({"_id": ObjectId(self.parking_slot_id)}, {"$set": {"is_occupied": True}})
        return self.short_id

    @staticmethod
    def view_bookings(user_id):
        bookings = db.bookings.find({"user_id": ObjectId(user_id)})
        booking_list = list(bookings)
        if not booking_list:
            return "No bookings found"
        
        formatted_bookings = []
        for booking in booking_list:
            parking_slot = db.parking_slots.find_one({"_id": ObjectId(booking["parking_slot_id"])})
            if not parking_slot:
                continue
            parking_space = db.parking_spaces.find_one({"_id": ObjectId(parking_slot["space_id"])})
            if not parking_space:
                continue
            formatted_booking = {
                "Booking ID": booking["short_id"],
                "Parking Space": parking_space["name"],
                "Parking Slot ID": parking_slot["short_id"],
                "Duration": booking["duration"],
                "Vehicle Type": booking["vehicle_type"],
                "License Plate": booking["license_plate"],
                "Payment Method": booking["payment_method"],
                "Amount Paid": booking["amount"]
            }
            formatted_bookings.append(formatted_booking)
        
        return formatted_bookings

    @staticmethod
    def delete_booking(short_id):
        booking = db.bookings.find_one({"short_id": short_id})
        if booking:
            db.parking_slots.update_one({"_id": ObjectId(booking["parking_slot_id"])}, {"$set": {"is_occupied": False}})
            db.bookings.delete_one({"short_id": short_id})
            return "Booking deleted successfully!"
        return "Booking not found!"

    @staticmethod
    def get_booking_id_by_short_id(short_id):
        booking = db.bookings.find_one({"short_id": short_id})
        if booking:
            return booking["_id"]
        return None

    @staticmethod
    def generate_statistic_report():
        total_bookings = db.bookings.count_documents({})
        total_hours = sum(booking['duration'] for booking in db.bookings.find({}))
        total_revenue = sum(booking['amount'] for booking in db.bookings.find({}))

        report = (
            f"Statistics Report:\n"
            f"Total Bookings: {total_bookings}\n"
            f"Total Hours Booked: {total_hours}\n"
            f"Total Revenue: ${total_revenue}\n"
        )
        return report

    @staticmethod
    def generate_revenue_report():
        total_revenue = sum(booking['amount'] for booking in db.bookings.find({}))
        
        report = (
            f"Revenue Report:\n"
            f"Total Revenue: ${total_revenue}\n"
        )
        return report
