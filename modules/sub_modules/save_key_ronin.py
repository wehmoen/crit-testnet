from modules.sub_modules import db
from cryptography.fernet import Fernet
import os
from modules import main
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from web3 import Web3

def get_decryption_key(password, salt):
    """Get decryption key from the KEK using PBKDF2"""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=350000)
    decryption_key = base64.urlsafe_b64encode(kdf.derive(password))

    return decryption_key
    
def find_value(line):
    """Find value for password and salt"""
    line_value = line.rstrip("\n")
    value = line_value[line_value.index("=") + 1 :]
    return value


def read_KEK():
    """Read KEK from a file stored on disk"""
    with open("data\kek.txt", "r") as f:
        for line in f:
            if line.startswith("password"):
                password = bytes(find_value(line), "utf-8")
            if line.startswith("salt"):
                salt = bytes(find_value(line), "utf-8")
    return password, salt

def generate_salt():
    return os.urandom(16)


def encrypt_pvt_key(pvt_key):
    """Encrypt private key"""
    """Using KEK to encrypt key"""
    password,salt= read_KEK()
    if salt ==b'':
       salt = generate_salt()
       print(f"Generated salt is:{salt}")

    decryption_key = get_decryption_key(password,salt)
    
    f = Fernet(decryption_key)
    fernet_token = f.encrypt(bytes(pvt_key, "utf-8"))
    return fernet_token
    
def fn_pvt_key(input_mode=0, pvt=""):
    """Adding users private key"""
    if input_mode == 0:
        pvt_key = input(
            "Please enter your private key. Or leave it blank to go back to main menu.\n"
        )
        return encrypt_pvt_key(pvt_key)
    else:
        return encrypt_pvt_key(pvt)


def ronin_add():
    """Adding users ronin"""
    ron_add = input("Please enter your ronin address.\n")
    return ron_add


def add_gas():
    """Adding gas price for the buy"""
    gas = input(
        "Please enter your desired gas price. Or leave blank for default price.\n"
    )
    if gas == "":
        gas = 1
    return gas


def add_key_address(input_mode=0, pvt="", ron="", gas=0):
    """Save ronin and private keys"""
    if input_mode == 0:
        pvt_key = fn_pvt_key()
        ron_add = ronin_add()
        gas_price = add_gas()
        if fn_pvt_key == "":
            return pvt_key()

        if ron_add == "":
            return ronin_add()
        else:
            db.execute(
                "INSERT INTO keys(pvt_key,ron_add,gas,fernet_key) VALUES(?,?,?,?)",
                pvt_key[0],
                ron_add,
                gas_price,
            )
            db.commit()
            print("Save Successfully!")
    else:
        
        address = ron.replace("ronin:", "0x")

        if Web3.isAddress(address):
            encrypted_pvt_key = fn_pvt_key(input_mode, pvt)
            if gas == "":
                gas = 20
            db.execute(
                "INSERT INTO keys(pvt_key,ron_add,gas,status) VALUES(?,?,?,?)",
                encrypted_pvt_key,
                ron,
                gas,
                "active"
            )
            db.commit()
            print("Ronin account is added to database.")
        else:
            print("Please enter a valid ronin address...")

def set_active(ron_add):
    """Set ronin account as active"""
    db.execute("UPDATE keys SET status=?","")
    db.commit()
    db.execute("UPDATE keys SET status=? WHERE ron_add =?","active",ron_add)
    db.commit()
    print(f"{ron_add} account is set as active! Please restart the bot to save changes.")

def get_active():
    """Get the active ronin account"""
    key_data = db.records("SELECT * FROM keys WHERE status =?","active")
    db.commit
    ronin_acc = key_data[0][1]
    return ronin_acc