from datetime import datetime


class CombinedServices:
    def __init__(self, mongodb_service, x_service, config):
        self.mongodb_service = mongodb_service
        self.x_service = x_service
        self.twitter_user_id = config["TWITTER_USER_ID"]

    def post_draft_tweet(self, draft_tweet_record_id):
        # Get the draft tweet record from MongoDB
        draft_tweet = self.mongodb_service.get_record(
            table_id="candidate_tweets",  # Use the correct collection name
            record_id=draft_tweet_record_id,
        )

        if not draft_tweet:
            return {"error": "Draft tweet not found"}, 404

        # Get the tweet content
        tweet_content = draft_tweet.get("content_cleaned") or draft_tweet.get("content")

        if not tweet_content:
            return {"error": "No content found in draft tweet"}, 400

        # Post the tweet
        tweet_id = self.x_service.post_tweet(tweet_content)

        # Update the MongoDB record
        tweet_url = f"https://x.com/{self.twitter_user_id}/status/{tweet_id}"
        updated_fields = {
            "tweet_url": tweet_url,
            "tweet_date": datetime.now().isoformat(),
        }
        self.mongodb_service.update_record(
            table_id="candidate_tweets",  # Use the correct collection name
            record_id=draft_tweet_record_id,
            fields=updated_fields,
        )

        return {"success": True, "tweet_id": tweet_id, "tweet_url": tweet_url}
