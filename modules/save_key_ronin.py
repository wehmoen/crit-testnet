from . import db
from cryptography.fernet import Fernet
import os
from modules import main

def generate_salt():
    return os.urandom(16)


def encrypt_pvt_key(pvt_key):
    """Encrypt private key"""
    """Using KEK to encrypt key"""
    password,salt= main.read_KEK()
    if salt ==b'':
       salt = generate_salt()
       print(f"Generated salt is:{salt}")

    decryption_key = main.get_decryption_key(password,salt)
    
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
        encrypted_pvt_key = fn_pvt_key(input_mode, pvt)
        if gas == "":
            gas = 20
        db.execute(
            "INSERT INTO keys(pvt_key,ron_add,gas) VALUES(?,?,?)",
            encrypted_pvt_key,
            ron,
            gas
        )
        db.commit()
        print("Ronin account is added to database.")

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