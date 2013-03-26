from google.appengine.ext import db


class Tweets(db.Model):
    user = db.StringProperty()
    user_id = db.TextProperty()
    user_name = db.TextProperty()
    tweet = db.TextProperty()
    timestamp = db.StringProperty()
    iso = db.StringProperty()
    source = db.StringProperty()
    geo = db.StringProperty()
    pic = db.StringProperty()


class TweetStreamed(db.Model):
    user = db.TextProperty()
    user_id = db.TextProperty()
    user_name = db.TextProperty()
    tweet = db.TextProperty()
    timestamp = db.StringProperty()
    iso = db.StringProperty()
    source = db.StringProperty()
    geo = db.StringProperty()
    pic = db.StringProperty()
