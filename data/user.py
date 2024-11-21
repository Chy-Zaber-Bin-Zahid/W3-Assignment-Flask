from werkzeug.security import generate_password_hash


users = [
    "admin@example.com": {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": generate_password_hash("adminpass"),
        "role": "Admin",
    },
    "user@example.com": {
        "name": "Regular User",
        "email": "user@example.com",
        "password": generate_password_hash("userpass"),
        "role": "User",
    }
]