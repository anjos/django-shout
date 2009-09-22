#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 16 Mar 2009 18:32:11 CET 

"""Introduces tags to facilitate the placement of "subscription links"
"""

from django import template
register = template.Library()

from shout.forms import SubscriptionForm

@register.inclusion_tag('shout/subscribe.html')
def subscribe():
  return { 'subscribe_form': SubscriptionForm() }

