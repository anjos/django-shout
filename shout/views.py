#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Thu 20 Nov 11:41:27 2008 

"""Specialized views for annouments.
"""

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from shout.models import *
from shout.forms import *
from shout.mail import *

@permission_required('shout.view_list')
def view_all(request):
  """Show all announcement lists."""
  lists = List.objects.all()
  if len(lists) == 1: #if there is only one list, show it entirely
    HttpResponseRedirect(reverse('shout-view-one',
      kwargs={'slug': lists[0].slug}))
  return render_to_response('shout/lists.html',
                            { 'object_list': lists, },
                            context_instance=RequestContext(request))

@permission_required('shout.view_list')
def view_one(request, slug):
  """Show specific announcement list."""
  return render_to_response('shout/list.html',
                            { 'object': List.objects.get(slug=slug), },
                            context_instance=RequestContext(request))

@permission_required('shout.view_list')
def view_mail(request, msgid):
  """Show specific announcement list e-mail."""
  return render_to_response('shout/email.html',
                            { 'object': Message.objects.get(id=msgid), },
                            context_instance=RequestContext(request))

@permission_required('shout.email_list')
def mail(request, slug, msgid=None):
  """Mail an announcement list."""
  l = List.objects.get(slug=slug)
  if request.method == "POST":
    form = EmailForm(request.POST)
    if form.is_valid():
      obj = form.save(commit=False)
      obj.list = l
      obj.by = request.user
      obj.save()
      mail_list(request, obj)
      return HttpResponseRedirect(reverse('shout-view-one', 
        kwargs={'slug': slug}))

  else:
    if msgid: 
      msg = Message.objects.get(id=msgid)
      form = EmailForm(initial={'subject': msg.subject, 'message': msg.message})
    else: form = EmailForm()
  return render_to_response('shout/mail_list.html',
                            { 
                              'object': l, 
                              'form': form, 
                            },
                            context_instance=RequestContext(request))

def subscribe(request, slug):
  """Subscribe to announcement list."""
  l = List.objects.get(slug=slug)
  if request.method == "POST":
    form = SubscriptionForm(request.POST)
    if form.is_valid():
      obj = form.save(commit=False)
      obj.list = l
      obj.language = 'fr'
      obj.save()
      mail_subscription(request, obj)
      mail_subscription_admin(request, obj)
      return render_to_response('shout/subscribe_thanks.html',
                                { 'object': obj, },
                                context_instance=RequestContext(request))
  # you cannot come directly
  raise Http404

def unsubscribe(request, slug):
  """Subscribe to announcement list."""
  l = List.objects.get(slug=slug)

  if request.method == "POST":
    form = UnsubscriptionForm(request.POST)
    if form.is_valid():
      obj = Member.objects.get(list=l, email=form.cleaned_data['email'])
      obj.delete()
      mail_unsubscription_admin(request, obj)
      return render_to_response('shout/unsubscribe_thanks.html',
                                { 'object': obj, },
                                context_instance=RequestContext(request))
  else:
    form = UnsubscriptionForm() 
  return render_to_response('shout/unsubscribe.html',
                            { 
                              'object': l, 
                              'form': form, 
                            },
                            context_instance=RequestContext(request))
