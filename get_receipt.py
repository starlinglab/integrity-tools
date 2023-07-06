
#!/usr/bin/python3
import json
import sys
import integrity.backend_db_indexed

h = sys.argv[1]
st = integrity.backend_db_indexed.database_index("/mnt/integrity_store/starling")


data = st.find_receipt(h)

receipt=st.get_receipt(h)
print (json.dumps(receipt))
