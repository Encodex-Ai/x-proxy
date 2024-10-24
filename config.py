import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists, otherwise Replit should still load its secrets
load_dotenv()


class Config:
    # OAuth 2.0 credentials
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    REDIRECT_URI = os.environ["REDIRECT_URI"]

    # OAuth 1.0a credentials
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

    # Other configurations
    API_SECRET_KEY = os.environ["API_SECRET_KEY"]
    TWITTER_USER_ID = os.environ["TWITTER_USER_ID"]

    # MongoDB configurations
    MONGODB_URI = os.environ["MONGODB_URI"]
    MONGODB_DB_NAME = os.environ["MONGODB_DB_NAME"]
    MONGODB_COLLECTION_NAME = os.environ["MONGODB_COLLECTION_NAME"]
    MONGODB_CANDIDATE_TWEETS_COLLECTION_NAME = os.environ[
        "MONGODB_CANDIDATE_TWEETS_COLLECTION_NAME"
    ]
