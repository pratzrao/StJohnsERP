import bcrypt
from services.db_helper import fetch_user, fetch_user_roles

def authenticate_user(email, password):
    """
    Authenticate the user by email and password.
    """
    user = fetch_user(email)

    if not user:
        return False, "User does not exist.", None
    if not user["is_active"]:
        return False, "Account is inactive.", None

    # Verify the password hash
    if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
        return False, "Incorrect password.", None

    # Fetch user roles
    roles = fetch_user_roles(user["user_type_id"])
    user["roles"] = roles

    return True, None, user