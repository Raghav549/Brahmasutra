# 🕉️ ब्रह्म AI Database निर्माता VERSION 18

import os
import sqlite3


class ब्रह्मDatabaseनिर्माता:

    def __init__(self):

        self.base_path = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_database")

        os.makedirs(self.base_path, exist_ok=True)

    def निर्मित(self, name):

        db_path = os.path.join(self.base_path, name + ".db")

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
        """)

        conn.commit()

        conn.close()

        print("Database निर्मित:", db_path)

        return db_path


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global builder, name

    print("🕉️ ब्रह्म AI Database निर्माता VERSION 18 सक्रिय")


    # test run

    builder = ब्रह्मDatabaseनिर्माता()

    name = input("Database नाम लिखें: ")

    builder.निर्मित(name)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
