"""Scratch for testing."""
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://twitter:0iNKWU6DMrvMNL6v@twitterbot-h85qm.mongodb.net/test")
db = client.twitterdb

with open("arff_header.arff", 'r') as header, open("twitter_bots.arff", 'w') as out:
    for row in header.readlines():
        out.write(row)
    out.write('\n')

    for doc in db.data.find():
        out.write("% {}\n".format(doc["user"]))
        vals = []
        data = json.loads(doc["data"])
        first = True
        for k in data:
            if first:
                first = False
                continue
            val = data[k]
            if val is True:
                val = 't'
            elif val is False:
                val = 'f'
            vals.append(str(val))
        vals.append(doc["type"])
        out.write("{}\n".format(",".join(vals)))

