from pymongo import MongoClient, errors
from pymongo.collection import Collection
from typing import Optional, List, Dict, Any


class MongoDBService:
    def __init__(self, config: Dict[str, str]) -> None:
        try:
            self.client = MongoClient(config["MONGODB_URI"])
            self.db = self.client[config["MONGODB_DB_NAME"]]
            self.candidate_table_id = config["MONGODB_CANDIDATE_TWEETS_COLLECTION_NAME"]
            self.draft_table_id = config["MONGODB_DRAFT_TWEETS_COLLECTION_NAME"]
            self.tables = {
                self.draft_table_id: self.db[self.draft_table_id],
                self.candidate_table_id: self.db[self.candidate_table_id],
            }
        except errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_table(self, table_id: str) -> Optional[Collection]:
        return self.tables.get(table_id)

    def get_records(
        self,
        table_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sort: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        try:
            collection = self.get_table(table_id)
            query = filter if filter else {}
            cursor = collection.find(query)
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except errors.PyMongoError as e:
            print(f"Error fetching records: {e}")
            return []

    def get_record(self, table_id: str, record_id: Any) -> Optional[Dict[str, Any]]:
        try:
            collection = self.get_table(table_id)
            return collection.find_one({"_id": record_id})
        except errors.PyMongoError as e:
            print(f"Error fetching record: {e}")
            return None

    def insert_record(self, table_id: str, record: Dict[str, Any]) -> Optional[Any]:
        try:
            collection = self.get_table(table_id)
            result = collection.insert_one(record)
            return result.inserted_id
        except errors.PyMongoError as e:
            print(f"Error inserting record: {e}")
            return None

    def update_record(
        self, table_id: str, record_id: Any, fields: Dict[str, Any]
    ) -> Optional[int]:
        try:
            collection = self.get_table(table_id)
            result = collection.update_one({"_id": record_id}, {"$set": fields})
            return result.modified_count
        except errors.PyMongoError as e:
            print(f"Error updating record: {e}")
            return None

    def delete_record(self, table_id: str, record_id: Any) -> Optional[int]:
        try:
            collection = self.get_table(table_id)
            result = collection.delete_one({"_id": record_id})
            return result.deleted_count
        except errors.PyMongoError as e:
            print(f"Error deleting record: {e}")
            return None

    def get_candidate_tweets(self) -> List[Dict[str, Any]]:
        return self.get_records(
            table_id=self.candidate_table_id,
            filter={"type": "candidate"},
            sort=[("id", 1)],
            limit=50,
        )
