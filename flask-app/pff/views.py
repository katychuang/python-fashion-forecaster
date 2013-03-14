from frame import app
from models import Tweets
from decorators import login_required

from flask import render_template, flash, url_for, redirect
from flaskext import wtf
from flaskext.wtf import validators

from google.appengine.api import users
from google.appengine.ext import db

import nltk, datetime
#import twitter

class PostForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    content = wtf.TextAreaField('Content', validators=[validators.Required()])

@app.route('/')
def redirect_to_home(): 
	#return redirect(url_for('index')) 
    return render_template('home.html')

@app.route('/twitter')
def list_tweets():  
	#api = twitter.Api()
	statuses = "" #api.GetPublicTimeline()
	return render_template('list_tweets.html', statuses=statuses)
	
@app.route('/posts')
def list_posts():
    posts = Post.all()
    return render_template('list_posts.html', posts=posts)

@app.route('/posts/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,
                    content = form.content.data,
                    author = users.get_current_user())
        post.put()
        flash('Post saved on database.')
        return redirect(url_for('list_posts'))
    return render_template('new_post.html', form=form)

@app.errorhandler(404)
#@with_nav_items
def page_not_found(e):
    """ Renders 404 Error page """

    context = {}

    return render_template('404.html', **context), 404

@app.route('/news')
def news():
    return render_template('newsfeed.html')

# Project: Python Fashion Forecaster
# Author: @katychuang
# Description: Takes data from GQL datastore based on 1 parameter and shows top words.
# Demo at http://style-buzz.appspot.com
@app.route('/topwords')
def topwords():

    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.probability import FreqDist
    from nltk.corpus import stopwords 

    ## place tweets into engligh and non english bins 
    ru = db.GqlQuery("SELECT * FROM Tweets where iso!=:1", 'en').fetch(limit=None)
    en = db.GqlQuery("SELECT * FROM Tweets where iso=:1", 'en').fetch(limit=None)

    corpus = ""

    freq1 = FreqDist()
    freq2 = FreqDist()

    for t in ru:
        corpus = nltk.word_tokenize(t.tweet)
        for a in corpus:
            freq1.inc(a)

    for t in en:
        corpus = nltk.word_tokenize(t.tweet)
        for a in corpus:
            freq2.inc(a)

    #display results
    bins = freq1.B() #Returns: The total number of sample values (or bins) that have counts > 0
    f1 = freq1.items()[:90] #Returns: List of all items in tuple format
    f2 = freq2.items()[:90]

    context = {'one': f1, 'two': f2}

    return render_template('topwords.html', **context)

@app.route('/keywords')
def keywords():
    return render_template('keywords.html')

@app.route('/brands')
def brands():
    return render_template('brands.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/cron')
def cron():
    #print "THE CRON PAGE IS RUNNING"
    import cron 

    context = {"abcdefghik": "cron job is up and running",
               "left_title": "Status of Cron Jobs",
               "right_title": "Data Captured",
               "xyz": cron.savetweets("")#,
              # "userxyz": cron.SpecificUser("")
               } 

    return render_template('index.html', **context)
