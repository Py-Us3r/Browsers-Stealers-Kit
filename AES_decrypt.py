from Crypto.Cipher import AES
import sys


#result="1|https://www.instagram.com/|testing|763130bdf32f7f15f0e0d465d1d9efddfea8cfe8c9888528fc747d2465e229b1332a015a5e0e|01fdfe3de68aa38ae2a417d0853264dae9daf48eae6be2cd72eb6b105eb77ac7"


result=sys.argv[1]
secret_key=result.split("|")[-1]
url=result.split("|")[1:][:-1][::4]
user=result.split("|")[2:][::4]
crypt_text=result.split("|")[3:][::4]



def decrypt_password(crypt_text,secret_key):

   try:
        crypt_text=bytes.fromhex(crypt_text)
        secret_key=bytes.fromhex(secret_key)
        initialisation_vector = crypt_text[3:15]
        encrypted_password = crypt_text[15:-16]
        cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
        decrypted_pass = cipher.decrypt(encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
   except:
      return "Incompatible Chrome Version"


print("\n"+"*"*82)
for url,user,crypt_text in zip(url,user,crypt_text):
    print(f"Url: {url}\n")
    print(f"Username: {user}\n")
    print(f"Password: {decrypt_password(crypt_text,secret_key)}\n")
    print("*"*82+"\n")




        

