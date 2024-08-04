from data_access.database import get_database

db = get_database()

class User:
    def __init__(self, username, password, role='customer'):  # Default role is 'customer'
        self.username = username
        self.password = password
        self.role = role

    def create_user(self):
        if db.users.find_one({"username": self.username}):
            return "Username already exists!"
        db.users.insert_one({"username": self.username, "password": self.password, "role": self.role})
        return "User created successfully!"

    def login_user(self):
        user = db.users.find_one({"username": self.username, "password": self.password})
        if user:
            return user["_id"], user["role"]  # Return user_id and role
        return None, None

    def logout_user(self):
        return "Logged out successfully!"
