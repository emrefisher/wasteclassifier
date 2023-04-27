import sqlite3
import uuid


def write_item(name: str):
    con = sqlite3.connect("items.db")
    cur = con.cursor()

    uid = str(uuid.uuid4()).replace('-', '')
    cur.execute("INSERT INTO items VALUES (?, ?)", (uid, name))
    con.commit()
