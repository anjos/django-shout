#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sex 17 Abr 2009 16:24:13 CEST 

"""Forms for announcement lists
"""

from django.forms import Form, ModelForm, fields, widgets
from django.utils.translation import ugettext_lazy as _
from shout.models import *

class SubscriptionForm(ModelForm):

  class Meta:
    model = Member
    exclude = ('joined', 'list', 'language')

class UnsubscriptionForm(Form):

  email = fields.EmailField(_(u'e-mail'))

  class Media:
    css = {'screen': ('shout/style.css',)}

class EmailForm(ModelForm):

  class Meta:
    model = Message
    exclude = ('list', 'sent', 'by')

  class Media:
    css = {'screen': ('shout/style.css',)}

