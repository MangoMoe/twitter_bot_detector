import tweepy

CONSUMER_KEY = 	"lH6LtU3XbHIrm1fjA9VGgZUgJ"
CONSUMER_SECRET = "k2bDhO2eOteZ4QqH8XXNBLRuC45nPWjEgRxahhFJ0p0Iu7GyBK"
ACCESS_TOKEN = "930275298829934593-a2Alnd6HjOwWvNU1NAEUfjybDPGBcYp"
ACCESS_SECRET = "i0cep5aNVs5tTtlxwFHkG6PzVsUrXpYkJknN5GHEpT4oc"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitter = tweepy.API(auth)


user = twitter.get_user("MogleTanner")
# print(user.screen_name)
print(twitter.user_timeline("MogleTanner"))

# user = twitter.get_user("MogleTanner"))
# mongo_db_object.insert_one(user._json)
