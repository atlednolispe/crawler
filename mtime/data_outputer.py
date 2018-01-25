import pymongo


class DataOutput:
    def __init__(self, collection):
        """
        Connect to MongoDB.
        """
        self.client = pymongo.MongoClient('192.168.3.3', 27017)
        self.db = self.client.mtime
        self.collection = self.db[collection]
        self.data = []

    def store_data(self, data):
        self.data.append(data)
        if len(self.data) > 9:
            self._store_to_collection()

    def _store_to_collection(self):
        self.collection.insert(self.data)
        self.data = []

    def store_flush(self):
        """
        Called when procedure end, store all datas lefted in self.data to database.
        """
        if self.data:
            self.collection.insert(self.data)
            self.data = []

