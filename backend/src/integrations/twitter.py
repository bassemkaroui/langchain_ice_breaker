import requests
import tweepy

from ..config import Config
from ..schemas.user import CLIUser

config = Config()


def scrape_user_tweets(username: str, num_tweets: int = 5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and
    returns them as a list of dictionaries. Each dictionary has two fields:
    "text" and "url".
    """

    twitter_client = tweepy.Client(
        bearer_token=config.twitter_bearer_token,
        consumer_key=config.twitter_api_key,
        consumer_secret=config.twitter_api_key_secret,
        access_token=config.twitter_access_token,
        access_token_secret=config.twitter_access_token_secret,
    )

    tweet_list = []

    if mock:
        EDEN_TWITTER_GIST = (
            "https://gist.githubusercontent.com/emarco177/827323bb5995"
            "53d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/"
            "eden-marco-twitter.json"
        )
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()

    else:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        )
        tweets = tweets.data

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    user = CLIUser(full_name="elonmusk")
    tweets = scrape_user_tweets(username=user.full_name, mock=True)
    print(tweets)
