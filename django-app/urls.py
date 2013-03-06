from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('wpe.prototype.urls')),
    url(r'^search/$', 'wpe.prototype.views.search'),

    url(r'^contact/thankyou/', 'wpe.prototype.views.thankyou'),
    url(r'^contact/', 'wpe.prototype.views.contactview'),


    # admin:
    url(r'^admin/', include(admin.site.urls)),

)

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment these two lines to enable your static files on PythonAnywhere
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

