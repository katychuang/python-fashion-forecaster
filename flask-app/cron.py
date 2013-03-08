# The URL Fetch library
from google.appengine.api import urlfetch
import simplejson, urllib 
import unicodedata

# Our tweets model
from frame import app
from frame.models import Tweets

def savetweets(object): 
    
    twitterurl = "http://search.twitter.com/search.json?q=fashion"
    # feed = urlfetch.fetch(twitterurl)

    result = simplejson.load(urllib.urlopen(twitterurl))

    for item in result['results']: 
        
        tStore = Tweets(user_id=item['from_user'])
        tStore.user = item['from_user']
        tStore.user_id = str(item['from_user_id'])
        tStore.user_name = unicodedata.normalize('NFKD', item['from_user_name']).encode('ascii','ignore')
        tStore.tweet = unicodedata.normalize('NFKD', item['text']).encode('ascii','ignore')
        tStore.timestamp = item['created_at']
        tStore.iso = item['iso_language_code'] 
        tStore.source = item['source']
        tStore.geo = str(item['geo']) #Property geo must be a str or unicode instance, not a dict
        tStore.pic = item['profile_image_url']
         
        tStore.put()

    return "{0}: {1}".format(tStore.user, tStore.tweet)  

# Detects if it is a URL link and adds the HTML tags
def linkify(text):
    # If http is present in, add the link tag
    if "http" in text:
        text = "&lt;a href='" + text + "'&gt;" + text + "&lt;/a&gt;"
    # If @ is present, turn it into a twitter handle link
    elif "@" in text:
        text = "&lt;a href='http://twitter.com/#!/" + text.split("@")[1] + "'&gt;" + text 
        text+= "&lt;/a&gt;"
    # Turn into twitter hash tags 
    elif "#" in text:
        text = "&lt;a href='https://twitter.com/#!/search/%23" + text.split("@")[1] + "'&gt;" + text 
        text+= "&lt;/a&gt;"
        
    return text


## Below for specific Users

def SpecificUser(users):
    
    #eventually pass in this list
    fashionistas = ['OfficialALT', 'wmag', 'Hillary_Kerr', 'Jess_Stam', 'MMBVogue']

    for u in fashionistas:
        t = 'https://api.twitter.com/1/statuses/user_timeline.json?screen_name={0}&count=100'.format(u)
        #url = urlfetch.fetch(t)
        result1 = simplejson.load(urllib.urlopen(t))

        for item in result1: 
            
            tStore = Tweets(user_id=u)
            tStore.tweet = unicodedata.normalize('NFKD', item['text']).encode('ascii','ignore')
            tStore.timestamp = item['created_at']
            tStore.iso = item['lang'] 
            tStore.source = item['source']
            tStore.geo = str(item['geo']) #Property geo must be a str or unicode instance, not a dict


            tStore.user = u
            # for i in item['user']:
            #     tStore.user_id = i.get('id_str', '')
            #     tStore.user_name = i.get('screen_name', '')
            #     tStore.pic = i.get('profile_image_url', '') 
             
# "in_reply_to_status_id": null,
# "in_reply_to_status_id_str": null,
# "in_reply_to_user_id": null,
# "in_reply_to_user_id_str": null,
# "in_reply_to_screen_name": null, 
# "retweet_count": 96, 

            tStore.put()

    return "{0}: {1}".format(u, tStore.tweet) 

