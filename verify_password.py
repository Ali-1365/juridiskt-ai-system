import bcrypt
import sys

def verify_password(plain_password, hashed_password):
    """
    Verify if a plain text password matches a hashed password
    
    Args:
        plain_password (str): The plain text password
        hashed_password (str): The hashed password to compare against
        
    Returns:
        bool: True if passwords match, False otherwise
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        stored_hash = hashed_password.encode('utf-8')
        
        print(f"Plain password: {plain_password}")
        print(f"Plain password length: {len(plain_password)}")
        print(f"Hashed password: {hashed_password}")
        print(f"Hashed password length: {len(hashed_password)}")
        
        is_valid = bcrypt.checkpw(password_bytes, stored_hash)
        print(f"Password valid: {is_valid}")
        return is_valid
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

if __name__ == "__main__":
    # Test with our current hash
    current_hash = "$2b$12$kMFnBzN/0xvxpdHc.bMQq.SVlpfW4iuaiJetyzvwxID/c4FgzGXla"
    
    # Test password
    test_password = "test123"
    
    # Verify
    is_valid = verify_password(test_password, current_hash)
    print(f"Result: {is_valid}")
    
    # Generate a new hash for the password
    password_bytes = test_password.encode('utf-8')
    salt = bcrypt.gensalt()
    new_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    print(f"New hash for '{test_password}': {new_hash}")
    
    # Verify with new hash
    is_valid_new = verify_password(test_password, new_hash)
    print(f"Result with new hash: {is_valid_new}")