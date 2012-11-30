from django.shortcuts import render_to_response, get_object_or_404
from prototype.models import Users, Tweets 
from django.template import RequestContext, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django import forms 

import re

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
    
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['tweet', 'user'])
        found_entries = Tweets.objects.filter(entry_query).order_by('-timestamp')

    return render_to_response('prototype/index.html',
                          { 'query': query_string, 'results': found_entries },
                          context_instance=RequestContext(request))

# Create your views here.
def home(request):
    dt = datetime.timedelta(days=1)
    today = datetime.date.today()
    series = [i*0.1 for i in range(10)]
    timeSeries = map(str, [today - i*dt for i in reversed(range(10))])
    rand = [random.random() for i in range(10)]
    sqrt = [math.sqrt(i*0.1) for i in range(10)]
    data = {'x': series, 'y': rand}
    timeSeriesData = {'x': timeSeries, 'y': rand}

    allmsgs = list(Tweets.objects.all())
    import numpy
    import nltk
    from collections import defaultdict
    wordFreqs = defaultdict(lambda: 0)

    #for item in allmsgs:
    #    tokens = nltk.word_tokenize(item)
    #    for word in tokens:
    #        wordFreqs[word] += 1

    return render_to_response('prototype/index.html', {'series': sqrt, 'topwords': [],
                                },context_instance=RequestContext(request))
    #return render_to_response('prototype/index.html')

def thankyou(request):
    return render_to_response('prototype/thankyou.html')

