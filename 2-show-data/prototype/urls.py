from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from wpe.prototype.models import Users,Tweets

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Tweets.objects.order_by('-timestamp')[:10],
            context_object_name='userlist',
            template_name='prototype/index.html')),
    #url(r'style/$', 'prototype.views.home'),
)
