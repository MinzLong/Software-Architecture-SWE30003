import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from business_logic.booking import Booking
from business_logic.payment import Visa, Cash
from business_logic.report import FactoryReport
from business_logic.vehicle import Vehicle
from data_access.parking import ParkingSlot, ParkingSpace
from data_access.user import User
from data_access.invoice import Invoice
from data_access.database import create_collections

# Initialize the collections and create default data
create_collections()
ParkingSpace.create_spaces()
ParkingSlot.create_slots()

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again.")

def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    user = User(username, password)
    user_id, role = user.login_user()
    
    if user_id:
        print("Login successful!")
        user_menu(user_id, role)
    else:
        print("Invalid username or password.")

def register():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    print("\nChoose role:")
    print("1. Admin")
    print("2. Customer")
    role_choice = input("Enter your choice: ").strip()
    
    if role_choice == "1":
        role = "admin"
    elif role_choice == "2":
        role = "customer"
    else:
        print("Invalid role choice, defaulting to customer.")
        role = "customer"
    
    user = User(username, password, role)
    result = user.create_user()
    print(result)

def user_menu(user_id, role):
    while True:
        print("\nUser Menu:")
        print("1. Create Booking")
        print("2. View Bookings")
        print("3. Delete Booking")
        print("4. Generate Report")
        print("5. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            create_booking(user_id)
        elif choice == "2":
            view_bookings(user_id)
        elif choice == "3":
            delete_booking(user_id)
        elif choice == "4":
            if role != 'admin':
                print("Access denied: Only admins can generate reports.")
                continue
            generate_report()
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice, please try again.")

def create_booking(user_id):
    print("\nAvailable Parking Spaces:")
    spaces = ParkingSpace.view_spaces()
    for space in spaces:
        print(f"Space ID: {space['short_id']}, Name: {space['name']}")
    
    space_short_id = input("Enter Parking Space ID: ").strip()
    space_id = ParkingSpace.get_space_id_by_short_id(space_short_id)
    
    if space_id:
        print("\nAvailable Parking Slots:")
        slots = ParkingSlot.view_slots(space_id)
        for slot in slots:
            print(f"Slot ID: {slot['short_id']}, Occupied: {'Yes' if slot['is_occupied'] else 'No'}")
        
        slot_short_id = input("Enter Parking Slot ID: ").strip()
        slot_id = ParkingSlot.get_slot_id_by_short_id(slot_short_id)
        
        if slot_id:
            duration = int(input("Enter duration in hours: ").strip())
            
            print("\nChoose vehicle type:")
            print("1. Car")
            print("2. Motorbike")
            vehicle_choice = input("Choose vehicle type: ").strip()
            if vehicle_choice == "1":
                vehicle_type = "Car"
            elif vehicle_choice == "2":
                vehicle_type = "Motorbike"
            else:
                print("Invalid vehicle type")
                return
            
            license_plate = input("Enter License Plate: ").strip()
            vehicle = Vehicle(vehicle_type, license_plate)
            
            amount = duration * 10  # Assuming $10 per hour
            print(f"You have to pay ${amount} for {duration} hours.")
            
            print("\nPayment Methods:")
            print("1. Visa")
            print("2. Cash")
            payment_method_choice = input("Choose payment method: ").strip()
            
            if payment_method_choice == "1":
                payment_method = Visa()
            elif payment_method_choice == "2":
                payment_method = Cash()
            else:
                print("Invalid payment method.")
                return
            
            booking = Booking(user_id, slot_id, duration, vehicle, payment_method, amount)
            booking_short_id = booking.create_booking()
            if booking_short_id:
                print(f"Booking created successfully! Booking ID: {booking_short_id}")
                booking_id = Booking.get_booking_id_by_short_id(booking_short_id)
                invoice = Invoice(booking_id=booking_id, amount=amount)
                print(invoice.create_invoice())
            else:
                print("Failed to create booking")
        else:
            print("Invalid Parking Slot ID.")
    else:
        print("Invalid Parking Space ID.")

def view_bookings(user_id):
    bookings = Booking.view_bookings(user_id)
    if isinstance(bookings, list):
        if not bookings:
            print("You don't have any bookings.")
        else:
            for booking in bookings:
                print(f"Booking ID: {booking['Booking ID']}")
                print(f"Parking Space: {booking['Parking Space']}")
                print(f"Parking Slot ID: {booking['Parking Slot ID']}")
                print(f"Duration: {booking['Duration']} hours")
                print(f"Vehicle Type: {booking['Vehicle Type']}")
                print(f"License Plate: {booking['License Plate']}")
                print(f"Payment Method: {booking['Payment Method']}")
                print(f"Amount Paid: ${booking['Amount Paid']}")
                print("-" * 20)
    else:
        print(bookings)

def delete_booking(user_id):
    booking_short_id = input("Enter Booking ID to delete: ").strip()
    result = Booking.delete_booking(booking_short_id)
    print(result)

def generate_report():
    print("\nReport Types:")
    print("1. Statistics Report")
    print("2. Revenue Report")
    report_type = input("Enter report type: ").strip()
    
    report = FactoryReport.create_report(report_type)
    
    if report:
        if report_type == "1":
            result = Booking.generate_statistic_report()
        elif report_type == "2":
            result = Booking.generate_revenue_report()
        else:
            result = report.generate()
        
        print(result)
    else:
        print("Invalid report type.")

if __name__ == "__main__":
    main_menu()
