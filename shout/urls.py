#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Wed 15 Apr 23:26:54 2009 

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^$', 'shout.views.view_all',
                         name='shout-view'),
                       url(r'^(?P<slug>[\w\.\-]+)/$',
                         'shout.views.view_one', 
                         name='shout-view-one'),
                       url(r'^(?P<slug>[\w\.\-]+)/mail/$',
                         'shout.views.mail', 
                         name='shout-mail'),
                       url(r'^(?P<slug>[\w\.\-]+)/mail/(?P<msgid>[\d]+)/$',
                         'shout.views.mail', 
                         name='shout-mail'),
                       url(r'^mail/(?P<msgid>[\d]+)/$',
                         'shout.views.view_mail', 
                         name='shout-view-mail'),
                       url(r'^(?P<slug>[\w\.\-]+)/subscribe/$',
                         'shout.views.subscribe', 
                         name='shout-subscribe'),
                       url(r'^(?P<slug>[\w\.\-]+)/unsubscribe/$',
                         'shout.views.unsubscribe', 
                         name='shout-unsubscribe'),
                       )

