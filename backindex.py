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
    cursorCollection = db['cursor']
    cursor_dict = cursorCollection.find_one()
    cursor = cursor_dict['data'] if cursor_dict else None
    try:
        url = '%s?cursor=%s' % (BYTE_URL, cursor) if cursor else BYTE_URL
        r = requests.get(url)
        data = r.json()['data']
    except Exception, e:
        print 'Failed to get latest posts from Byte: %s' % str(e)
        return

    cursor = data['cursor']
    if cursorCollection.find_one():
        cursorCollection.replace_one({}, {'data': cursor})
    else:
        cursorCollection.insert_one({'data': cursor})

    for post in data['posts']:
        post['_id'] = post['id']
        db['posts'].save(post)
    print 'Done indexing'

if __name__ == '__main__':
    sched.start()

