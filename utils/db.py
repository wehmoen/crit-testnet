from sqlite3 import connect


# tables
# snipe_list - table for sniping list 
#    fields - name,pur_price,filter,num_asset
# keys - table for private keys
# 	 fields- pvt_key,ron_add,gas,fernet_key

DB_PATH = "./sniperbot.db"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()

def commit():
	cxn.commit()


def close():
	cxn.close()

def execute(command, *values):
	cur.execute(command, tuple(values))

def records(command, *values):
	cur.execute(command, tuple(values))

	return cur.fetchall()

# cur.execute("""
# 		DELETE FROM keys WHERE ron_add = "Test"
# """)

# cur.execute("SELECT * FROM keys")

# print(cur.fetchall())
# cxn.commit()
# cxn.close()