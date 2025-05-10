# In-memory user database (for simplicity)
user_db = {}

def sign_up(firstname: str, lastname: str, username: str, email: str, password: str, confirm_password: str) -> bool:
    # Check if password and confirm password match
    if password != confirm_password:
        print("Passwords do not match.")
        return False  # Passwords don't match

    # Store user details in the 'database'
    if email in user_db:
        print("Email already in use.")
        return False  # User already exists
    else:
        # Store the user data (password stored as plaintext, not secure in a real-world scenario)
        user_db[email] = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'password': password
        }
        print("Sign up request:")
        print(f"  First Name: {firstname}")
        print(f"  Last Name: {lastname}")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"  Confirm Password: {confirm_password}")
        print(f"User {username} signed up successfully.")
        return True

def log_in(email: str, password: str) -> bool:
    print(f"Log in request - email: {email}")
    
    # Check if email exists in our "database"
    if email in user_db:
        # Compare the password
        if user_db[email]['password'] == password:
            print("Login successful!")
            return True
        else:
            print("Incorrect password.")
            return False
    else:
        print("Email not found.")
        return False
