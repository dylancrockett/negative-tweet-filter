"""
    This program uses a combination of the twitter API and the textblob library to perform
    sentiment analysis of 100 tweets which have a specific hashtag.

    This allows the user to pick the category and find positive tweets within that category.
"""

import textblob
import requests
import json
import os
from typing import List

bearer_token = os.getenv("TWITTER_TOKEN")


def get_tweets(query: str, count=100, lang: str = "en"):
    # make twitter API call
    response = requests.get("https://api.twitter.com/1.1/search/tweets.json",
                            params={
                                "q": query,
                                "count": str(count),
                                "lang": lang,
                                "result_type": "recent",
                                "tweet_mode": "extended"
                            },
                            headers={"Authorization": "Bearer " + bearer_token})

    # return tweet data as a list
    return [x for x in response.json()["statuses"]]


# checks if a given tweet is negative
def is_negative(tweet: dict, pol_min: float = 0.25) -> bool:
    blob = textblob.TextBlob(tweet["full_text"])

    polarity = blob.sentiment[0]

    if pol_min > polarity:
        return True
    return False


# save a list of tweets
def save_tweets(tweets: List[dict], filename: str):
    with open(filename + ".json", "w", encoding="utf-8") as f:
        # dump tweet list to file
        json.dump(tweets, f, indent=4, ensure_ascii=False)


# main function
def main():
    # get twitter query
    query = input("Please input your twitter Query (ex. '#dogecoin' or '@discord'): ")

    # get tweets based on query
    tweets = get_tweets(query, 100)

    # filter negative tweets
    tweets = [x for x in tweets if not is_negative(x)]

    # make tweet data easier to use
    tweets = [
        {
            "created_at": x["created_at"],
            "id": x["id"],
            "text": x["full_text"]
        } for x in tweets
    ]

    # save tweets
    save_tweets(tweets, "positive_tweets")

    print("\nTweets saved to file 'positive_tweets.json'.")


if __name__ == "__main__":
    main()
