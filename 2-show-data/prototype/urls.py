from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from prototype.models import Users,Tweets

urlpatterns = patterns('',
	url(r'^$', 'wpe.prototype.views.home', name='random-series'),
)