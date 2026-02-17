# ब्रह्म डेटाबेस जनक
# VERSION 119
# Automatic Database Generator

import os
import sqlite3


class ब्रह्मडेटाबेसजनक:

    def __init__(self, मूलपथ):

        self.मूलपथ = मूलपथ

        self.dbpath = os.path.join(मूलपथ, "database")

        if not os.path.exists(self.dbpath):
            os.makedirs(self.dbpath)

        self.dbfile = os.path.join(self.dbpath, "brahma.db")

        print("ब्रह्म डेटाबेस जनक सक्रिय")


    def जनन(self, आर्किटेक्चर):

        if not आर्किटेक्चर["database"]:
            print("डेटाबेस आवश्यक नहीं")
            return

        self.create_db()

        print("डेटाबेस जनन पूर्ण")


    def create_db(self):

        conn = sqlite3.connect(self.dbfile)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """)

        conn.commit()

        conn.close()
