from django.shortcuts import render_to_response, get_object_or_404
from wpe.prototype.models import Users, Tweets, ContactForm
# from django.http import Http404
from django.template import RequestContext, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError

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


# Create your views here.
def home(request):
    return render_to_response('prototype/index.html', {'poll': ''})

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

def contactview(request):
    subject = request.POST.get('topic', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['katychuang@acm.org'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thankyou/')
    else:
        return render_to_response('prototype/contact.html', {'form': ContactForm()})

    return render_to_response('prototype/contact.html', {'form': ContactForm()},
			context_instance=RequestContext(request))

def thankyou(request):
    return render_to_response('prototype/thankyou.html')