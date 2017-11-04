from flask import Flask, redirect, render_template, request
import feedparser
import uuid
from datetime import datetime
from time import mktime

app = Flask(__name__)

posts = {}

# Wrapper function for readability
def new_uuid():
    return uuid.uuid4().hex

def contains_key(key, dict):
    return dict.get(key) != None

def sort_feeds(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x[2] < pivot[2]:
                less.append(x)
            if x[2] == pivot[2]:
                equal.append(x)
            if x[2] > pivot[2]:
                greater.append(x)
        return sort_feeds(less)+equal+sort_feeds(greater)
    else:
        return array

def to_datetime(t_struct):
    return datetime.fromtimestamp(mktime(t_struct))

# Returns a vector of titles, links and dates for a given url
def urls_data(urls):
    lts = []
    for url in urls:
        d = feedparser.parse(url)
        for post in d.entries:
            lts.append([post.title, post.link, to_datetime(post.published_parsed)])
    return lts

def process_urls(urls):
    data = urls_data(urls)
    sorted_data = sort_feeds(data)
    return reversed(sorted_data)

# Redirects to new perma if none specified
@app.route('/')
def index():
    new_route = "/" + new_uuid()
    return redirect(new_route)

# Main app logic happens here
@app.route('/<id>', methods=["GET", "POST"])
def perma(id):
    # Add new id to posts dict if it does not already exist
    if not contains_key(id, posts):
        posts[id] = []

    if request.method == "POST":
        new_link = request.form["new_link"]
        posts[id].append(new_link) 

    return render_template("perma.html", post_to=id, posts=process_urls(posts[id]))

app.run()
