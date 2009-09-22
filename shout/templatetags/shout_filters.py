#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sat 18 Apr 17:20:19 2009 

"""Filters
"""

from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
def email_from(o):
  """Returns something like "First Last" <user@address> from the user
  object."""
  return u'%s <%s>' % (o.get_full_name(), o.email)
