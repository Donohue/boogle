#!/usr/bin/env python
import json
import requests
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient

BYTE_URL = 'https://api.byte.co/v1/posts/latest'
client = MongoClient(os.environ['MONGOLAB_URI'])
db = client.get_default_database()
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def main():
    print 'Indexing'
    try:
        r = requests.get(BYTE_URL)
        data = r.json()['data']
    except Exception, e:
        print 'Failed to get latest posts from Byte: %s' % str(e)
        return

    for post in data['posts']:
        post['_id'] = post['id']
        db['posts'].save(post)
    print 'Done indexing'

if __name__ == '__main__':
    sched.start()

