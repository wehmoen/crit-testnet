from sqlite3 import connect


# tables
# snipe_list - table for sniping list
#    fields - name,pur_price,filter,num_asset,link,buy_count
# keys - table for private keys
# 	 fields- pvt_key,ron_add,gas,fernet_key,status
# verify - table for verifying access to the app
# 	 fields- user_name,prod_stat


DB_PATH = "sniperbot.db"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def commit():
    cxn.commit()


def close():
    cxn.close()


def execute(command, *values):
    """Execute and SQL Queries"""
    cur.execute(command, tuple(values))


def records(command, *values):
    """Fetch records on query"""
    cur.execute(command, tuple(values))

    return cur.fetchall()

# cur.execute("DELETE from keys")
# cur.execute("DELETE from snipe_list")
# # print(cur.fetchall())
# cxn.commit()
# cxn.close()
