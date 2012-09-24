# A simple Twitter feed scraper and parser

# modified version of 
# https://gist.github.com/978125

import tweet
import simplejson
import urllib2



def read_tweets(user, num_tweets):
    tweets = []
    url = "http://api.twitter.com/1/statuses/user_timeline.json?\
           screen_name=%s&count=%s&include_rts=true" % (user, num_tweets)
    file = urllib2.urlopen(url)
    content = file.read()
    json = simplejson.loads(content) 

    for js_tweet in json:
        t = tweet.Tweet()
        t.id = js_tweet['id']
        t.username = js_tweet['user']['screen_name']

        try:
            t.retweet_user = js_tweet['retweeted_status']['user']['screen_name']
            t.retweeted = True
        except:
            t.retweeted = False

        t.set_date(js_tweet['created_at']) 
        t.set_tweet_url() 
        t.set_text(js_tweet['text']) 
        t.set_profile_url()

        tweets.append(t)

    return tweets


def save_tweets():

    people = ['python', 'pyladies']

    import MySQLdb
    db = MySQLdb.connect(host="mysql.server", # your host, usually localhost
                        user="username", # your username
                        passwd="pw", # your password
                        db="databasename") # name of the data base

    cur = db.cursor()
 

    for person in people:
        count = 50 # this is the number of tweets to read from user
        tweets = read_tweets(person, count)
        for t in tweets:
           s = "insert into TABLE_NAME (user, tweet, timestamp) values ('" + t.username + "', '" + t.html_text + "', '" + str(t.date) + "');"
            try:
               cur.execute(s)
               db.commit()
           except:
               print "SQL Insert Error" 

    print 'Script saved tweets successfully.'


save_tweets()