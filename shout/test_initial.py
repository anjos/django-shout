#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 20 Abr 2009 19:20:47 CEST 

"""Initial data for tests
"""
import os
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.conf import settings
from shout.models import *
import random, datetime

def create_site():
  s = Site()
  s.name = 'Test Site'
  s.domain = 'www.example.com'
  s.save()

def create_admin_user():
  admin = User()
  admin.username = 'admin'
  admin.is_superuser = True
  admin.email = 'admin@example.com'
  admin.first_name = 'Admin'
  admin.last_name = 'User'
  admin.set_password('admin')
  admin.save()

def create_group(name):
  g = Group()
  g.name = name
  g.save()

def create_users(n, group):
  comite = User()
  comite.username = 'comite'
  comite.email = 'comite@example.com'
  comite.first_name = 'Comite'
  comite.last_name = 'User'
  comite.set_password('comite')
  comite.save()
  comite.groups.add(Group.objects.get(name=group))
  comite.save()
  for i in range(n):
    member = User()
    member.username = 'member%d' % (i+1)
    member.email = 'member%d@example.com' % (i+1)
    member.first_name = 'Member'
    member.last_name = '%d' % (i+1)
    member.set_password('member')
    member.save()

def set_permissions(group):
  q = Q(name__contains='list') | \
      Q(name__contains='member') | \
      Q(name__contains='message')
  group.permissions = Permission.objects.filter(q)
  group.save()

def create_members(l, n):
  for i in range(n):
    member = Member()
    member.name = 'Member Number %d' % i
    member.mobile = ''
    member.email = 'member%d@example.com' % i
    member.list = l
    member.language = 'fr'
    member.save()

def create_messages(l, n, by):
  for i in range(n):
    m = Message()
    m.subject = 'Subject of message %d' % i
    m.message = 'This is my nice message %d\nHave fun!' % i
    m.by = by 
    m.list = l
    m.save()

def populate_db():

  #print 'Creating test site'
  create_site()
  #print 'Creating test admin user'
  create_admin_user()
  #print 'Creating test groups'
  create_group('privileged')
  #print 'Creating test users'
  create_users(5, 'privileged')

  #print 'Setting specific permissions'
  set_permissions(Group.objects.get(name='privileged'))
  #print 'Creating lists'
  l1 = List.objects.create(name='List One', slug='list1')
  l2 = List.objects.create(name='List Two', slug='list2')
  #print 'Creating members'
  create_members(l1, 15)
  create_members(l2, 10)
  #print 'Creating messages'
  by = User.objects.get(username='admin')
  create_messages(l1, 5, by)
  create_messages(l2, 15, by)
