# A simple Twitter feed scraper and parser

# copied from https://gist.github.com/978125

import time
from datetime import datetime
import re


class Tweet():
    """Store the tweet info
    """
    id = None
    username = None
    url = None
    user_avatar_url = None
    tweet_url = None
    profile_url = None
    html_text = None
    retweeted = None
    retweet_user = None
    date = None
    desc = None
    name = None

    def set_date(self, date_str):
        """Convert string to datetime
        """
        time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")#Tue Apr 26 08:57:55 +0000 2011
        self.date = datetime.fromtimestamp(time.mktime(time_struct))


    def set_text(self, plain_text):
        """convert plain text into html text with http, user and hashtag links
        """

        if "'" in plain_text: plain_text = re.sub("'", "\\'", plain_text)

        re_http = re.compile(r"(http://[^ ]+)")
        self.html_text = re_http.sub(r'\1', plain_text)

        re_https = re.compile(r"(https://[^ ]+)")
        self.html_text = re_https.sub(r'\1', self.html_text)


        re_user = re.compile(r'@[0-9a-zA-Z+_]*',re.IGNORECASE)
        for iterator in re_user.finditer(self.html_text):
            a_username = iterator.group(0)
            username = a_username.replace('@','')
            link = '' + a_username + ''
            self.html_text = self.html_text.replace(a_username, link)


        re_hash = re.compile(r'#[0-9a-zA-Z+_]*',re.IGNORECASE)
        for iterator in re_hash.finditer(self.html_text):
            h_tag = iterator.group(0)
            link_tag = h_tag.replace('#','%23')
            link = '' + h_tag + ''
            self.html_text = self.html_text.replace(h_tag + " ", link + " ")
            #check last tag
            offset = len(self.html_text) - len(h_tag)
            index = self.html_text.find(h_tag, offset)
            if index >= 0:
                self.html_text = self.html_text[:index] + " " + link


    def set_profile_url(self):
        """Create the url profile
        """
        if self.retweeted:
            self.profile_url = "http://www.twitter.com/%s" % self.retweet_user
        else:
            self.profile_url = "http://www.twitter.com/%s" % self.username

    def set_tweet_url(self):
        """Create the url of the tweet
        """
        self.tweet_url = "http://www.twitter.com/%s/status/%s" % (self.username, self.id)

