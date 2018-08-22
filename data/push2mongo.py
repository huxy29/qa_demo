# encoding: utf-8


from pymongo import MongoClient
import json


client1 = MongoClient(host='localhost', port=27017)
db1 = client1['vags']
coll1 = db1['article']


client2 = MongoClient(host='10.156.88.30', port=8078)
db2 = client2['articles_backup']
coll2 = db2['video']


def main():
    cursor = coll2.find({"releaseTimeStamp": {"$gt": 1533052800}}).limit(100)
    for doc in cursor:
        del doc['_id']
        coll1.insert_one(doc)
        print 'insert_one'



if __name__ == '__main__':
    main()