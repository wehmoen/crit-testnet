
from utils import db
from cryptography.fernet import Fernet

def pvtkey(input_mode=0,pvt=""):
    """Adding Users private key"""
    if input_mode==0:
        pvt_key = input(
            "Please enter your private key. Or leave it blank to go back to main menu.\n")
        
        # Encrypt Private Key
        # fernet_key should also be saved somewhere to be able to decrypt the data
        fernet_key = Fernet.generate_key()
        f = Fernet(fernet_key)
        fernet_token = f.encrypt(bytes(pvt_key, 'utf-8'))
        return fernet_token,fernet_key

    else:
        # Encrypt Private Key
        # fernet_key should also be saved somewhere to be able to decrypt the data
        fernet_key = Fernet.generate_key()
        f = Fernet(fernet_key)
        fernet_token = f.encrypt(bytes(pvt, 'utf-8'))
        return fernet_token,fernet_key


def ronin_add():
    """Adding users ronin"""
    ron_add = input(
        "Please enter your ronin address.\n")
    return ron_add

def add_gas():
    """Adding Gas Price for the buy"""
    gas= input("Please enter your desired gas price. Or leave blank for default price.\n")
    if gas == "":
        gas = 1
    return gas

def add_key_address(input_mode=0,pvt="",ron="",gas=0):
    """Save ronin and private keys"""
    if input_mode==0:
        pvt_key=pvtkey()
        ron_add =ronin_add()
        gas_price = add_gas()
        if pvtkey=="":
            return pvt_key()
        
        if ron_add=="":
            return ronin_add()
        else:
            db.execute("INSERT INTO keys(pvt_key,ron_add,gas,fernet_key) VALUES(?,?,?,?)",pvt_key[0],ron_add,gas_price,pvt_key[1])
            db.commit()
            print("Save Successfully!")
    else:
        pvt_key=pvtkey(input_mode,pvt)
        db.execute("INSERT INTO keys(pvt_key,ron_add,gas,fernet_key) VALUES(?,?,?,?)",pvt_key[0],ron,gas,pvt_key[1])
        db.commit()
        print("Saved from GUI")
