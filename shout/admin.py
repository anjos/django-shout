#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Wed 15 Apr 23:24:37 2009 

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from shout.models import * 

def members(object):
  return object.member_set.count()
members.short_description = _(u'Members')

def last_subscription(object):
  members = object.member_set.order_by('-joined')
  if members: return members[0].joined
  else: return _(u'No subscriptions yet!')
last_subscription.short_description = _(u'Last subscription')

class ListAdmin(admin.ModelAdmin):
  list_display = ('__unicode__', 'creation', members, last_subscription)
  list_filter = ('creation', ) 
  model = List

class MemberAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'mobile', 'list', 'joined')
  list_filter = ('name', 'email')
  model = Member

class MessageAdmin(admin.ModelAdmin):
  list_display = ('subject', 'list', 'sent', 'by')
  list_filter = ('subject', 'list', 'by')
  model = Message 

admin.site.register(List, ListAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Message, MessageAdmin)
