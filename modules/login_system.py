# ==========================================================
# Buddy AI - Login System
# Local Account Manager
# ==========================================================

import os
import json
import hashlib
import secrets


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

ACCOUNT_FILE = os.path.join(
    DATA_DIR,
    "account.json"
)


# ==========================================================
# CREATE DATA FOLDER
# ==========================================================

def ensure_data_folder():

    if not os.path.exists(DATA_DIR):

        os.makedirs(
            DATA_DIR,
            exist_ok=True
        )


# ==========================================================
# CHECK ACCOUNT
# ==========================================================

def account_exists():

    return os.path.isfile(
        ACCOUNT_FILE
    )


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(
    password,
    salt
):

    password_bytes = password.encode(
        "utf-8"
    )

    salt_bytes = salt.encode(
        "utf-8"
    )

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt_bytes,
        100_000
    )

    return hashed.hex()


# ==========================================================
# SAVE ACCOUNT
# ==========================================================

def create_account(
    name,
    username,
    password
):

    ensure_data_folder()

    name = str(name).strip()
    username = str(username).strip()
    password = str(password)

    if not name:

        return False, "Name enter karein."

    if not username:

        return False, "Username enter karein."

    if not password:

        return False, "Password enter karein."

    if len(password) < 4:

        return False, (
            "Password kam az kam "
            "4 characters ka hona chahiye."
        )

    if account_exists():

        return False, (
            "Buddy account already exist karta hai."
        )

    salt = secrets.token_hex(
        16
    )

    password_hash = hash_password(
        password,
        salt
    )

    account_data = {

        "name": name,

        "username": username,

        "password_hash": password_hash,

        "salt": salt,

        "remember_login": True,

        "logged_in": True

    }

    try:

        with open(
            ACCOUNT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                account_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True, (
            "Account successfully create ho gaya."
        )

    except Exception as e:

        print(
            "Account Save Error:",
            repr(e)
        )

        return False, (
            "Account save nahi ho saka."
        )


# ==========================================================
# LOAD ACCOUNT
# ==========================================================

def load_account():

    if not account_exists():

        return None

    try:

        with open(
            ACCOUNT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception as e:

        print(
            "Account Load Error:",
            repr(e)
        )

        return None


# ==========================================================
# VERIFY LOGIN
# ==========================================================

def verify_login(
    username,
    password
):

    account = load_account()

    if not account:

        return False, (
            "Buddy account nahi mila."
        )

    username = str(
        username
    ).strip()

    password = str(
        password
    )

    saved_username = account.get(
        "username",
        ""
    )

    salt = account.get(
        "salt",
        ""
    )

    saved_hash = account.get(
        "password_hash",
        ""
    )

    if username != saved_username:

        return False, (
            "Username ya password ghalat hai."
        )

    if not salt or not saved_hash:

        return False, (
            "Account data corrupt hai."
        )

    current_hash = hash_password(
        password,
        salt
    )

    if secrets.compare_digest(
        current_hash,
        saved_hash
    ):

        set_logged_in(
            True
        )

        return True, (
            "Login successful."
        )

    return False, (
        "Username ya password ghalat hai."
    )


# ==========================================================
# REMEMBER LOGIN
# ==========================================================

def set_remember_login(
    value
):

    account = load_account()

    if not account:

        return False

    account[
        "remember_login"
    ] = bool(value)

    try:

        with open(
            ACCOUNT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                account,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        print(
            "Remember Login Error:",
            repr(e)
        )

        return False


# ==========================================================
# SET LOGGED IN
# ==========================================================

def set_logged_in(
    value
):

    account = load_account()

    if not account:

        return False

    account[
        "logged_in"
    ] = bool(value)

    try:

        with open(
            ACCOUNT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                account,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        print(
            "Login State Error:",
            repr(e)
        )

        return False


# ==========================================================
# AUTO LOGIN CHECK
# ==========================================================

def should_auto_login():

    account = load_account()

    if not account:

        return False

    remember_login = account.get(
        "remember_login",
        False
    )

    logged_in = account.get(
        "logged_in",
        False
    )

    return (
        remember_login
        and
        logged_in
    )


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    return set_logged_in(
        False
    )


# ==========================================================
# GET USER NAME
# ==========================================================

def get_user_name():

    account = load_account()

    if not account:

        return ""

    return account.get(
        "name",
        ""
    )


# ==========================================================
# GET USERNAME
# ==========================================================

def get_username():

    account = load_account()

    if not account:

        return ""

    return account.get(
        "username",
        ""
    )


# ==========================================================
# DELETE ACCOUNT
# ==========================================================

def delete_account():

    if not account_exists():

        return False

    try:

        os.remove(
            ACCOUNT_FILE
        )

        return True

    except Exception as e:

        print(
            "Delete Account Error:",
            repr(e)
        )

        return False


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "================================"
    )

    print(
        "       BUDDY LOGIN SYSTEM"
    )

    print(
        "================================"
    )

    print(
        "Account exists:",
        account_exists()
    )

    if account_exists():

        print(
            "User:",
            get_user_name()
        )

        print(
            "Username:",
            get_username()
        )

        print(
            "Auto Login:",
            should_auto_login()
        )

    else:

        print(
            "No Buddy account found."
        )

    print(
        "================================"
    )