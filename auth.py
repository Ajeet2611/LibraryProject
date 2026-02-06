# auth.py
from db import get_connection
from security import check_password

def login(username=None, password=None):
    conn = get_connection()
    if conn is None:
        return None

    # CLI mode
    if username is None and password is None:
        username = input("Enter Username: ")
        password = input("Enter Password: ")

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT UserID, Username, Password, Role, InstitutionID
    FROM Users
    WHERE Username = %s
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return None

    # 🔐 Password verify
    if check_password(password, user["Password"]):
        return {
            "UserID": user["UserID"],
            "Username": user["Username"],
            "Role": user["Role"],
            "InstitutionID": user["InstitutionID"]
        }
    else:
        return None
