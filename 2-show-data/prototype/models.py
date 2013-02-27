from django.db import models
import datetime
import django.forms as forms
#from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError

# Create your models here.
class Users(models.Model):
    handle = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    link = models.CharField(max_length=100)

    def __unicode__(self):
        return self.handle


class Tweets(models.Model):
    user = models.CharField(max_length=80)
    tweet = models.CharField(max_length=160) #Tweets have 160 char to allow room for user/screennames
    timestamp = models.DateTimeField('date published')

    def __unicode__(self):
        return self.tweet

# A simple contact form with four fields.
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=Textarea())