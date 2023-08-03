import sqlite3

if __name__ == '__main__': 
    conn = sqlite3.connect('test.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS VECTOR_MAPPINGS
            (ID INT PRIMARY KEY     NOT NULL,
            PATH           TEXT    NOT NULL);''')
    conn.commit()
    conn.close()
