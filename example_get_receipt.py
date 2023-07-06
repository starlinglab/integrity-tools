#!/usr/bin/python3
import os
import json
import sys
import integrity.backend_db_indexed

target_hash = sys.argv[1]
db = integrity.backend_db_indexed.database_index("/mnt/integrity_store/starling")

# get basic info about the receipt
data = db.find_receipt(target_hash)
print (json.dumps(data,indent=2))

# get the receipt
receipt=db.get_receipt(target_hash)
print (json.dumps(receipt,indent=2))

# get the asset's filename (from inside the zip)
filename=db.get_asset_filename(target_hash)
print (filename)


# get the asset's filename (from inside the zip)
metadata=db.get_content_metadata(target_hash)
print (json.dumps(metadata.decode("UTF-8"),indent=2))

# save as receipt's id

# get value from receipt
target_filename = receipt["sourceId"]["value"]
target_ext=os.path.splitext(filename)[1]

content=db.get_asset(target_hash)
with open(f"/tmp/{target_filename}{target_ext}", "wb") as file:
    # Write the variable's contents to the file
    file.write(content)
print(f"wrote to /tmp/{target_filename}{target_ext}")
