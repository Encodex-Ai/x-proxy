from pymongo import MongoClient, errors


class MongoDBService:
    def __init__(self, config):
        try:
            self.client = MongoClient(config["MONGODB_URI"])
            self.db = self.client[config["MONGODB_DB_NAME"]]
            self.draft_tweets_collection = self.db[
                config["MONGODB_DRAFT_TWEETS_COLLECTION_NAME"]
            ]
            self.candidate_tweets_collection = self.db[
                config["MONGODB_CANDIDATE_TWEETS_COLLECTION_NAME"]
            ]

        except errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_records(self, filter=None, sort=None, limit=None):
        try:
            query = filter if filter else {}
            cursor = self.draft_tweets_collection.find(query)
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except errors.PyMongoError as e:
            print(f"Error fetching records: {e}")
            return []

    def get_record(self, record_id):
        try:
            return self.draft_tweets_collection.find_one({"_id": record_id})
        except errors.PyMongoError as e:
            print(f"Error fetching record: {e}")
            return None

    def insert_record(self, record):
        try:
            result = self.draft_tweets_collection.insert_one(record)
            return result.inserted_id
        except errors.PyMongoError as e:
            print(f"Error inserting record: {e}")
            return None

    def update_record(self, record_id, fields):
        try:
            result = self.draft_tweets_collection.update_one(
                {"_id": record_id}, {"$set": fields}
            )
            return result.modified_count
        except errors.PyMongoError as e:
            print(f"Error updating record: {e}")
            return None

    def delete_record(self, record_id):
        try:
            result = self.draft_tweets_collection.delete_one({"_id": record_id})
            return result.deleted_count
        except errors.PyMongoError as e:
            print(f"Error deleting record: {e}")
            return None

    def get_candidate_tweets(self):
        try:
            # Assuming candidate tweets are identified by a specific field, e.g., 'type': 'candidate'
            filter = {"type": "candidate"}
            sort = [("id", 1)]  # Sort by 'id' in ascending order
            limit = 50  # Limit to 50 records
            return self.get_records(filter=filter, sort=sort, limit=limit)
        except errors.PyMongoError as e:
            print(f"Error fetching candidate tweets: {e}")
            return []
