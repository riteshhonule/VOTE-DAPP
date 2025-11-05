import sqlite3

def init_db():
    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS votes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aadhaar TEXT,
                    email TEXT,
                    wallet TEXT,
                    party TEXT,
                    tx_hash TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def save_vote(aadhaar, email, wallet, party, tx_hash):
    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()
    c.execute("INSERT INTO votes (aadhaar, email, wallet, party, tx_hash) VALUES (?,?,?,?,?)",
              (aadhaar, email, wallet, party, tx_hash))
    conn.commit()
    conn.close()
