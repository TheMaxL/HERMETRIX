import sqlite3

def sign_up(firstname: str, lastname: str, username: str, email: str, password: str, confirm_password: str) -> bool:
    if password != confirm_password:
        print("Passwords do not match.")
        return False

    try:
        # Create a new connection in the current thread
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            # Insert user data
            cursor.execute(
                "INSERT INTO users (firstname, lastname, username, email, password) VALUES (?, ?, ?, ?, ?)",
                (firstname, lastname, username, email, password)
            )

            conn.commit()

        print(f"User {username} signed up successfully.")
        return True

    except sqlite3.IntegrityError:
        print("Email already in use.")
        return False

def log_in(email: str, password: str) -> bool:
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()

        if row:
            if row[0] == password:
                print("Login successful!")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Email not found.")
            return False

    except Exception as e:
        print("Error during login:", e)
        return False
