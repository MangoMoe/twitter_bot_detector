"""Script for extracting usernames from a mongodb of tweets"""
from pymongo import MongoClient

# TODO replace this with the address of jacob's mongodb server
# client = MongoClient("mongodb+srv://twitter:0iNKWU6DMrvMNL6v@twitterbot-h85qm.mongodb.net/test")
client = MongoClient("192.168.1.102:27017")
# client = MongoClient("ip, thingum (port)")
print("Connected to client")

# TODO replace with the name of the db with the info we want
db = client.twitter_corpus
tweets = db.tweets

# See the website
print("Finding")
tweets_iter = tweets.find({})   # justin says this will work?
print("Done Finding")
# scotts_posts = posts.find({'author': 'Scott'})

print("Reading user names")
usernames = []
count = 0
for tweet in tweets_iter:
    print(count)
    # print(tweet)
    # print(tweet['user']['screen_name'])
    usernames.append(tweet['user']['screen_name'])
    count += 1
    if count > 2000: break 
print("Done reading user names")

print("Writing to file")
with open("real_users.txt","w") as usernames_file:
    for username in usernames:
        usernames_file.write(username)
        usernames_file.write("\n")
print("Finished")
