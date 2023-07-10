#!/usr/bin/python3
import os
import json
import sys
import integrity.backend_db_indexed



# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Invalid number of arguments.")
    print("Usage: python script.py <source_organization_id> <target_folder>")
    sys.exit(1)
    
org_id  = sys.argv[1]
target_folder = sys.argv[2]
db_folder = "/mnt/integrity_store/starling"
source_folder = f"{db_folder}/internal/{org_id}"


if not os.path.exists(source_folder):
    print(f"Source folder '{source_folder}' does not exist.")
    sys.exit(1)

# Check if the target folder exists
if not os.path.exists(target_folder):
    print(f"Target folder '{target_folder}' does not exist.")
    sys.exit(1)

# Check if the target folder exists
if not os.path.exists(db_folder):
    print(f"Database folder  does not exist.")
    sys.exit(1)

db = integrity.backend_db_indexed.database_index("/mnt/integrity_store/starling")


# Loop through all files in the folder

# Loop through all the folders in the org
for collection_id in os.listdir(source_folder):

    # 
    source_folder_files = f"{db_folder}/internal/{org_id}/{collection_id}/action-archive"
    if os.path.exists(source_folder_files):
        # Check if folder exists, could be a temp file with no action-archive
        for asset in os.listdir(source_folder_files):

            # Only do zip files. Skip encrypted files
            if os.path.splitext(asset)[1] == ".zip": 

                # Get hash from filename           
                target_hash = os.path.splitext(asset)[0]
                metadata=json.loads(db.get_content_metadata(target_hash).decode("utf-8"))
                print(metadata)
                date_create=metadata["content-metadata"]["dateCreated"]

                # Get Receipt
                receipt=db.get_receipt(target_hash)
                # get target filename
                if "sourceId" not in receipt or "value" not in receipt["sourceId"]:
                    print(f"Missing sourceId for {target_hash}")
                    continue
                target_filename = receipt["sourceId"]["value"]

                # get name of asset inside zip file
                filename=db.get_asset_filename(target_hash)

                # get extension of file
                target_ext=os.path.splitext(filename)[1]

                # put together the final filename
                output_filename = f"{target_filename}{target_ext}"
                # put together the path where this file name will be stored
                output_path = f"{target_folder}/{collection_id}"

                # make the folder if it doesnt exist
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                # Final filename
                output_full_path=f"{output_path}/{output_filename}"

                # write the data
                print(f"Processing {target_hash} for file {output_full_path}")
                content=db.get_asset(target_hash)
                
                # Content
                with open(output_full_path, "wb") as file:
                    # Write the variable's contents to the file
                    file.write(content)
                # json
                with open(output_full_path + ".json", "w") as file:
                    # Write the variable's contents to the file
                    file.write(json.dumps(receipt,indent=2))
                