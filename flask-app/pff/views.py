from frame import app
from models import Tweets
from decorators import login_required

from flask import render_template, flash, url_for, redirect
from flaskext import wtf
from flaskext.wtf import validators

from google.appengine.api import users
from google.appengine.ext import db

import nltk, datetime, re, networkx
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


@app.route('/topwords')
def topwords():
"""
    inspired by
    http://www.huffingtonpost.com/brian-honigman/the-100-most-popular-hash_b_2463195.html

    used these resources
    http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
    http://text-processing.com/demo/sentiment/
    http://ravikiranj.net/drupal/201205/code/machine-learning/how-build-twitter-sentiment-analyzer

    http://fashionweekdates.com/world-fashion-week-dates-schedule.html


"""
    #import nltk
    from nltk.tokenize import word_tokenize
    from nltk.probability import FreqDist
    from nltk.corpus import stopwords

    ## place tweets into morning and afternoon bins
    ru = db.GqlQuery("SELECT * FROM Tweets where iso!=:1", 'en').fetch(limit=5000)
    en = db.GqlQuery("SELECT * FROM Tweets where iso=:1", 'en').fetch(limit=5000)
    #Tweets.get('timestamp'<=time)
    #botlist = db.GqlQuery('SELECT * FROM Weatherbot ORDER BY zipcode ASC')
    #pm = Tweets.get('timestamp'>time)

    #this method because nltk.corpus.stopwords.words('english') doesnt work in GAE

    stop = "a, about, above, across, after, again, against, all, almost, alone, along, already, also, although, always, am, among, an, and, another, any, anybody, anyone, anything, anywhere, are, area, areas, aren't, around, as, ask, asked, asking, asks, at, away, b, back, backed, backing, backs, be, became, because, become, becomes, been, before, began, behind, being, beings, below, best, better, between, big, both, but, by, c, came, can, cannot, can't, case, cases, certain, certainly, clear, clearly, come, could, couldn't, d, did, didn't, differ, different, differently, do, does, doesn't, doing, done, don't, down, downed, downing, downs, during, e, each, early, either, end, ended, ending, ends, enough, even, evenly, ever, every, everybody, everyone, everything, everywhere, f, face, faces, fact, facts, far, felt, few, find, finds, first, for, four, from, full, fully, further, furthered, furthering, furthers, g, gave, general, generally, get, gets, give, given, gives, go, going, good, goods, got, great, greater, greatest, group, grouped, grouping, groups, h, had, hadn't, has, hasn't, have, haven't, having, he, he'd, he'll, her, here, here's, hers, herself, he's, high, higher, highest, him, himself, his, how, however, how's, i, i'd, if, i'll, i'm, important, in, interest, interested, interesting, interests, into, is, isn't, it, its, it's, itself, i've, j, just, k, keep, keeps, kind, knew, know, known, knows, l, large, largely, last, later, latest, least, less, let, lets, let's, like, likely, long, longer, longest, m, made, make, making, man, many, may, me, member, members, men, might, more, most, mostly, mr, mrs, much, must, mustn't, my, myself, n, necessary, need, needed, needing, needs, never, new, newer, newest, next, no, nobody, non, noone, nor, not, nothing, now, nowhere, number, numbers, o, of, off, often, old, older, oldest, on, once, one, only, open, opened, opening, opens, or, order, ordered, ordering, orders, other, others, ought, our, ours, ourselves, out, over, own, p, part, parted, parting, parts, per, perhaps, place, places, point, pointed, pointing, points, possible, present, presented, presenting, presents, problem, problems, put, puts, q, quite, r, rather, really, right, room, rooms, s, said, same, saw, say, says, second, seconds, see, seem, seemed, seeming, seems, sees, several, shall, shan't, she, she'd, she'll, she's, should, shouldn't, show, showed, showing, shows, side, sides, since, small, smaller, smallest, so, some, somebody, someone, something, somewhere, state, states, still, such, sure, t, take, taken, than, that, that's, the, their, theirs, them, themselves, then, there, therefore, there's, these, they, they'd, they'll, they're, they've, thing, things, think, thinks, this, those, though, thought, thoughts, three, through, thus, to, today, together, too, took, toward, turn, turned, turning, turns, two, u, under, until, up, upon, us, use, used, uses, v, very, w, want, wanted, wanting, wants, was, wasn't, way, ways, we, we'd, well, we'll, wells, went, were, we're, weren't, we've, what, what's, when, when's, where, where's, whether, which, while, who, whole, whom, who's, whose, why, why's, will, with, within, without, won't, work, worked, working, works, would, wouldn't, x, y, year, years, yes, yet, you, you'd, you'll, young, younger, youngest, your, you're, yours, yourself, yourselves, you've, z"

    stopwordsenglish = re.findall(r'\w+', stop, flags = re.UNICODE | re.LOCALE)

    stopwordstwitter = ['http', '#', '@', '!', ':', ';', '&', '\'', '-',
                      't', 'co', 'rt']


    stopwords_list = stopwordsenglish + stopwordstwitter
    freq1 = FreqDist()
    freq2 = FreqDist()

    for t in ru:
        #We only want to work with lowercase for the comparisons
        sentence = t.tweet.lower()

        #remove punctuation and split into seperate words
        words = re.findall(r'\w+', sentence, flags = re.UNICODE | re.LOCALE)

        #corpus = nltk.word_tokenize(words)
        for a in words:
            if a not in stopwords_list:
                freq1.inc(a)

    for t in en:
        #We only want to work with lowercase for the comparisons
        sentence = t.tweet.lower()

        #remove punctuation and split into seperate words
        words = re.findall(r'\w+', sentence, flags = re.UNICODE | re.LOCALE)

        #corpus = nltk.word_tokenize(t.tweet)
        for a in words:
            if a not in stopwords_list:
                freq2.inc(a)

    #display results
    #bins = freq1.B()  # Returns: The total number of sample bins with counts > 0
    f1 = freq1.items()[:90]  # Returns: List of all items in tuple format
    f2 = freq2.items()[:90]

    context = {'one': f1, 'two': f2,
               'stop': stopwords_list
               }

    return render_template('topwords.html', **context)


@app.route('/topusers')
def topusers():
    ## place tweets into morning and afternoon bins
    userlist = db.GqlQuery("SELECT * FROM Tweets").fetch(limit=5000)

    context = {'users': userlist
               }

    return render_template('topusers.html', **context)


@app.route('/keywords')
def keywords():
    return render_template('keywords.html')


@app.route('/words')
def brands():
    return render_template('brands.html')


@app.route('/search')
def search():
    return render_template('search.html')


# Image Colors
# http://www.vijayp.ca/blog/2012/06/colours-in-movie-posters-since-1914/

@app.route('/map')
def map():

    geolist = db.GqlQuery("SELECT * FROM Tweets where geo!='None' AND geo> NULL")

    #{u'type': u'Point', u'coordinates': [-0.04915454758181264, 109.32146120063652]}
    points = []
    for g in geolist:
        points.append(g.geo[1])  # save coordinates only instead of whole string

    context = {'geolist': points}

    return render_template('map.html', **context)


@app.route('/cron')
def cron():
    #print "THE CRON PAGE IS RUNNING"
    import cron

    context = {"abcdefghik": "cron job is up and running",
               "left_title": "Status of Cron Jobs",
               "right_title": "Data Captured",
               "xyz": cron.savetweets("")
               }

    return render_template('index.html', **context)
