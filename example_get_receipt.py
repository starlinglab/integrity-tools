#!/usr/bin/python3
import json
import sys
import integrity.backend_db_indexed

target_hash = sys.argv[1]
db = integrity.backend_db_indexed.database_index("/mnt/integrity_store/starling")


data = db.find_receipt(target_hash)
print (json.dumps(data,indent=2))


receipt=db.get_receipt(target_hash)
print (json.dumps(receipt,indent=2))
