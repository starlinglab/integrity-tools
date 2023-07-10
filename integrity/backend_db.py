import zipfile
import os
import json


class database:
    starling_path = ""
    internal_cache = {}

    def __init__(self, starling_path) -> None:
        """
        Initialize the class, defining where the flat file databases

        :param straling_path: path the the starling folder containing the database. For example /mnt/integrity_store/starling
        """
        self.starling_path = starling_path

    def find_receipt(self, hash):
        """
        Returns an array array containing a dict path,org,collection and hash for a given hash

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        if hash in self.internal_cache:
            return self.internal_cache[hash]
        res = []
        for org in os.listdir(f"{self.starling_path}/shared"):
            if os.path.isdir(f"{self.starling_path}/shared"):
                for collection in os.listdir(f"{self.starling_path}/shared/{org}"):
                    if os.path.isdir(
                        f"{self.starling_path}/shared/{org}/{collection}/action-archive"
                    ):
                        for receipt in os.listdir(
                            f"{self.starling_path}/shared/{org}/{collection}/action-archive"
                        ):
                            receipt_file = open(
                                f"{self.starling_path}/shared/{org}/{collection}/action-archive/{receipt}",
                                "r",
                            )
                            receipt_string = receipt_file.read()
                            if receipt_string.find(hash) != -1:
                                v = {
                                    "path": f"{self.starling_path}/shared/{org}/{collection}/action-archive/{receipt}",
                                    "org": org,
                                    "collection": collection,
                                    "hash": os.path.splitext(receipt)[0],
                                }
                                res.append(v)
        self.internal_cache[hash] = res
        return res

    def get_asset_filename(self, hash):
        """
        Returns the filename of the asset for a specific hash. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        receipts = self.find_receipt(hash)
        if len(receipts) == 0:
            return None
        receipt = receipts[0]
        receipt_file = open(f"{receipt['path']}", "r")
        receipt_json = json.load(receipt_file)
        data_path = f"{self.starling_path}/internal/{receipt['org']}/{receipt['collection']}/action-archive/{receipt_json['archive']['sha256']}.zip"
        with zipfile.ZipFile(data_path) as zf:
            for filename in zf.namelist():
                if filename.startswith(f"{receipt_json['content']['sha256']}"):
                    if not filename.endswith(f".json"):
                        return filename

    def get_content(self, hash, suffix):
        """
        Returns the content of a file inside an asset's zip. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        receipts = self.find_receipt(hash)
        if len(receipts)==0:
            return None
        receipt= receipts[0]
        receipt_file=open(f"{receipt['path']}","r")
        receipt_json = json.load(receipt_file)
        datapath  = f"{self.starling_path}/internal/{receipt['org']}/{receipt['collection']}/action-archive/{receipt_json['archive']['sha256']}.zip"
        with zipfile.ZipFile(datapath) as zf:
            for filename in zf.namelist():
                if filename.endswith(suffix):
                    with zf.open(filename,"r") as f:
                        file = f.read()
                        return file


    def get_content_metadata(self, hash):
        """
        Returns the content metadata for a given hash. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        return self.get_content(hash, "-meta-content.json")

    def get_recorder_metadata(self, hash):
        """
        Returns the recorder metadata for a given hash. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        return self.get_content(hash, "-meta-recorder.json")

    def get_ots(self, hash):
        """
        Returns the ots file for a given hash. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """

        return self.get_content(hash, ".ots")

    def get_asset_authsign(self, hash):
        """
        Returns the content's authsign for a given hash. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        filename = self.get_asset_filename(hash)
        return self.get_content(hash, f"{filename}.authsign")
    
    def get_asset(self, hash):
        filename = self.get_asset_filename(hash)
        return self.get_content(hash, f"{filename}")

    def get_receipt(self, hash, index=0):
        """
        Returns the content of the receipt for a given hash. Returns none is not found.

        :param: hash: the hash to use to find the receipt. It can be any hash found in the receipt.
        """
        receipts = self.find_receipt(hash)
        if len(receipts) == 0:
            return None

        receipt_file = open(f"{receipts[index]['path']}", "r")
        receipt_json = json.load(receipt_file)
        return receipt_json
