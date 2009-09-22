#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sat 18 Apr 18:52:43 2009 

"""Tests for announcements
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import Group
import random

from shout.models import *
from shout.test_initial import populate_db 

def print_mail():
  if False: #switch this to avoid printing mail
    for i, m in enumerate(mail.outbox):
      print 'Mail %02d' % (i+1), 70*'='
      print m.message()
      print 78*'='

def get_status(client, url, username):
  if username: client.login(username=username, password=username)
  response = client.get(url)
  if username: client.logout()
  return response.status_code

class TestList(TestCase):

  def setUp(self):
    populate_db()
    self.client = Client()

  def test_view(self):
    views = [
        'shout-view', 
        ('shout-view-one', {'slug': 'list1'}),
        ('shout-mail', {'slug': 'list1'}),
        ]

    for v in views:
      if isinstance(v, str): url = reverse(v)
      else: url = reverse(v[0], kwargs=v[1])
      self.assertEqual(get_status(self.client, url, ''), 302) #redirect
      #to enable the next entry, create a 404.html template!
      #self.assertEqual(get_status(self.client, url, 'member3'), 404) #denied
      self.assertEqual(get_status(self.client, url, 'comite'), 200) #ok
      self.assertEqual(get_status(self.client, url, 'admin'), 200) #ok

  def test_subscribe(self):
    url = reverse('shout-subscribe', kwargs={'slug': 'list1'})
    post = { 
        'name': 'Edgar Raimundo', 
        'email': 'edgar@example.com', 
        'mobile': '+411212345667' 
        }
    response = self.client.post(url, post)
    self.assertTemplateUsed(response, 'shout/subscribe_thanks.html')
    self.assertEqual(len(mail.outbox), 2) #2 messages sent, member & committee
    print_mail()

  def test_unsubscribe(self):
    url = reverse('shout-unsubscribe', kwargs={'slug': 'list2'})
    post = { 
        'email': 'member1@example.com', 
        }
    response = self.client.post(url, post)
    self.assertTemplateUsed(response, 'shout/unsubscribe_thanks.html')
    self.assertEqual(len(mail.outbox), 1) #1 message sent to committee
    print_mail()

  def test_mail(self):
    url = reverse('shout-mail', kwargs={'slug': 'list2'})
    post = { 
        'subject': 'This is a test subject', 
        'message': 'Nothing much to say, what do you need?\n\nYES!', 
        }
    self.client.login(username='comite', password='comite')
    response = self.client.post(url, post)
    self.assertRedirects(response, reverse('shout-view-one', 
      kwargs={'slug': 'list2'}))
    self.assertEqual(len(mail.outbox), 1) #1 message sent to committee
    print_mail()
    self.client.logout()
