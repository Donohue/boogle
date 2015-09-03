import re
import os
from pymongo import MongoClient
from flask import Flask, make_response, render_template, redirect, abort, request, jsonify

app = Flask(__name__)
app.config['DEBUG'] = True
client = MongoClient(os.environ['MONGOLAB_URI'])
db = client.get_default_database()
db.posts.ensure_index([
    ('name', 1),
    ('caption', 1)
])

@app.route('/')
def homepage():
    q = request.args.get('q', None)
    posts = []
    if q:
        search_query = {"$or": [
            {"name": {"$regex": q}},
            {"caption": {"$regex": q}}
        ]}
        posts = db.posts.find(search_query)
    return render_template('index.html', posts=posts)

