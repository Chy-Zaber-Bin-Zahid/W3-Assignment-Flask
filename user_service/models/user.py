from werkzeug.security import generate_password_hash


users = [
    {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": generate_password_hash("adminpass"),
        "role": "Admin",
    },
    {
        "name": "Regular User",
        "email": "user@example.com",
        "password": generate_password_hash("userpass"),
        "role": "User",
    }
]
