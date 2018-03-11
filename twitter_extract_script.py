from __future__ import division
import tweepy
import json
import uuid
import random
import datetime
import collections
import jsonpickle

CONSUMER_KEY = 	"lH6LtU3XbHIrm1fjA9VGgZUgJ"
CONSUMER_SECRET = "k2bDhO2eOteZ4QqH8XXNBLRuC45nPWjEgRxahhFJ0p0Iu7GyBK"
ACCESS_TOKEN = "930275298829934593-a2Alnd6HjOwWvNU1NAEUfjybDPGBcYp"
ACCESS_SECRET = "i0cep5aNVs5tTtlxwFHkG6PzVsUrXpYkJknN5GHEpT4oc"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitter = tweepy.API(auth)

class twitter_data(object):
    def __init__(self, verified, url, protected, followers_count, friends_count, listed_count, favorites_count, statuses_count, contributors_enabled, default_profile, default_profile_image, quote_avg, retweet_avg, reply_avg, favorite_avg, user_mentions_avg, symbols_avg, urls_avg, hashtags_avg, media_avg, avg_num_tweets, tweet_regularity):
        self.verified = verified
        # TODO do we just want to store the url?
        self.url = url is not None
        self.protected = protected
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.listed_count = listed_count
        self.favorites_count = favorites_count
        self.statuses_count = statuses_count
        self.contributors_enabled = contributors_enabled
        self.default_profile = default_profile
        self.default_profile_image = default_profile_image
        self.quote_avg = quote_avg
        self.retweet_avg = retweet_avg
        self.reply_avg = reply_avg
        self.favorite_avg = favorite_avg
        self.user_mentions_avg = user_mentions_avg
        self.symbols_avg = symbols_avg
        self.urls_avg = urls_avg
        self.hashtags_avg = hashtags_avg
        self.media_avg = media_avg
        self.avg_num_tweets = avg_num_tweets
        # regularity is basically the mode of the time gaps between tweets, basically if it is greater than 1 that means they post with mechanical regularity (Known bots have high values for this, and the regular user I tested this on has 1)
        self.tweet_regularity = tweet_regularity

def get_data_object(user):
    # TODO maybe use more tweets?
    timeline = twitter.user_timeline(user.id, count=100)
    oldest_date = datetime.datetime.now()
    tweet_times = []
    quote_count = 0
    retweet_count = 0
    reply_count = 0
    favorite_count = 0
    user_mentions_count = 0
    symbols_count = 0
    urls_count = 0
    hashtags_count = 0
    media_count = 0

    # loop through tweets in timeline
    for tweet in timeline:
        if tweet.created_at < oldest_date:
            oldest_date = tweet.created_at
        tweet_times.append(tweet.created_at)
        # for some reason these don't work
        # quote_count += tweet.quote_count if tweet.quote_count is not None else 0
        # reply_count += tweet.reply_count
        retweet_count += tweet.retweet_count
        favorite_count += tweet.favorite_count if tweet.favorite_count is not None else 0
        entities = tweet.entities
        user_mentions_count += len(entities["user_mentions"]) if "user_mentions" in entities else 0
        symbols_count += len(entities["symbols"]) if "symbols" in entities else 0
        urls_count += len(entities["urls"]) if "urls" in entities else 0
        hashtags_count += len(entities["hashtags"]) if "hashtags" in entities else 0
        media_count += len(entities["media"]) if "media" in entities else 0

    # get the number of days old the oldest tweet is
    delta_time = datetime.datetime.now() - oldest_date
    # calculate time between tweets
    delta_times = []
    for i in range(len(tweet_times) -1):
        delta_times.append(tweet_times[i + 1] - tweet_times[i])
    counter = collections.Counter(delta_times)
    tweet_regularity = counter.most_common(1)[0][1]

    # Calculate averages
    quote_avg = quote_count / len(timeline)
    retweet_avg = retweet_count / len(timeline)
    reply_avg = reply_count / len(timeline)
    favorite_avg = favorite_count / len(timeline)
    user_mentions_avg = user_mentions_count / len(timeline)
    symbols_avg = symbols_count / len(timeline)
    urls_avg = urls_count / len(timeline)
    hashtags_avg = hashtags_count / len(timeline)
    media_avg = media_count / len(timeline)
    avg_num_tweets = len(timeline) / (delta_time.total_seconds() / (60 * 60 * 24))

    # Build and return return object
    ret_obj = twitter_data(user.verified, user.url, user.protected, user.followers_count, user.friends_count, user.listed_count, user.favourites_count, user.statuses_count, user.contributors_enabled, user.default_profile, user.default_profile_image, quote_avg, retweet_avg, reply_avg, favorite_avg, user_mentions_avg, symbols_avg, urls_avg, hashtags_avg, media_avg, avg_num_tweets, tweet_regularity)
    return ret_obj


with open('bots.txt', 'r') as bots:
    count = 0
    for line in bots.readlines():
        count += 1
        # user = twitter.get_user("MogleTanner")
        user = twitter.get_user(line.strip())
        twitter_data_obj = get_data_object(user)
        json = jsonpickle.encode(twitter_data_obj)
        other_data_obj = jsonpickle.decode(json)
        if twitter_data_obj.avg_num_tweets != other_data_obj.avg_num_tweets:
            print("CRAP THIS ISN'T WORKING")
        print("crap this worked!")
        print(json)

        # if count > 3:
        #     break
        break
    
        # mongo_db_object.insert_one(user._json)


# random_id = random_id % 10000000
# while True:
#     try:
#         # random_id = uuid.uuid4().int>>64 %  1000000000000000000
#         # random_id = uuid.uuid4().int>>64 %  100000000000000000
#         # random_id = uuid.uuid4().int & (1<<64)-1 %  1000000000000000000
#         # 932686855740338177
#         random_id = random.getrandbits(64) %  1000000000000000000
#         print("Generated id: \n{}\n{}".format(random_id, 932686855740338177))
#         user = twitter.get_user(random_id)
#         break
#     except tweepy.error.TweepError:
#         print("Failed to find a correct id, better try again")

# print("We found one")
# print(user.name)
# print(user.id)
# print(user.verified)
# print(user.url)
# print(user.protected)
# print(user.followers_count)
# print(user.friends_count)
# print(user.listed_count)
# print(user.favourites_count)
# print(user.statuses_count)
# print(user.contributors_enabled)
# print(user.default_profile)
# print(user.default_profile_image)