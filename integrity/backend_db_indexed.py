import json
import os
import sqlite3
import integrity.backend_db

class database_index(integrity.backend_db.database):
  

  sql_path =""
  def __init__(self, starling_path, sql_path = "/tmp/integrity.sql") -> None:
    integrity.backend_db.database.__init__(self,starling_path)
    self.sql_path=sql_path
    if os.path.exists(sql_path) == False:
      conn = sqlite3.connect(sql_path)
      cursor = conn.cursor()
      cursor.execute('''
        CREATE TABLE IF NOT EXISTS hash (
            hash TEXT PRIMARY KEY,
            json TEXT
        )
      ''')
      conn.close()
   
  def find_receipt(self, hash):

    conn = sqlite3.connect(self.sql_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hash WHERE hash=?", (hash,))
    row = cursor.fetchone()
    res = ""
    if row:
      res = json.loads(row[1])
    else:
      res = super().find_receipt(hash)
      if res: 
        json_res = json.dumps(res)
        cursor.execute(f"INSERT INTO hash (hash, json) VALUES (?, ?)", (hash, json_res))
        conn.commit()  # Commit the changes

    conn.close()
    return res