from pff import app
from models import Post
from decorators import login_required

from flask import render_template, flash, url_for, redirect
from flaskext import wtf
from flaskext.wtf import validators

from google.appengine.api import users

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

@app.route('/seasons')
def seasons():
    return render_template('seasons.html')

@app.route('/keywords')
def keywords():
    return render_template('keywords.html')

@app.route('/brands')
def brands():
    return render_template('brands.html')

@app.route('/search')
def search():
    return render_template('search.html')
