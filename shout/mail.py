#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sat 18 Apr 17:36:19 2009 

"""Mail utilities for announcements.
"""

from django.template import loader, RequestContext
from django.conf import settings
from django.core.mail import send_mail, mail_admins, mail_managers, EmailMessage
from django.utils import translation
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

def fix_apos(s):
  """Fix funny looking apostrophe thing from django"""
  return s.replace('&#39;',"'")

def mail_member(request, object, subject_template, message_template):
  """Mails a new member about some action."""
  context = RequestContext(request, {'object': object})
  translation.activate(object.language)
  subject = fix_apos(loader.render_to_string(subject_template, context))
  subject = subject.replace('\n','')
  message = fix_apos(loader.render_to_string(message_template, context))
  translation.deactivate()
  send_mail(subject=subject, message=message,
      from_email=settings.DEFAULT_FROM_EMAIL,
      recipient_list=(unicode(object),))

def mail_admin(request, object, recipients, subject_template, 
    message_template):
  """Mails managers summarizing something."""

  context = RequestContext(request, {'object': object})
  subject = fix_apos(loader.render_to_string(subject_template, context))
  subject = subject.replace('\n','')
  message = fix_apos(loader.render_to_string(message_template, context))
  to = []
  for r in recipients: to.append(u'%s <%s>' % (r[0], r[1]))
  send_mail(subject=subject, message=message,
      from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=to)

def mail_list(request, object):
  """This sends a mass mail with BCC to all and managers"""
  site = Site.objects.get_current()
  bcc = [o.email for o in object.list.member_set.all()] 
  for r in settings.MANAGERS: bcc.append(u'%s <%s>' % (r[0], r[1]))
  message = object.message
  message += u'\n--\n'
  message += _(u'You are receiving this e-mail because you are subscribed to %(list)s.\n' % {'list': unicode(o.list)}) 
  message += _(u'If you wish to unsubscribe, please visit: %(site)s%(uri)s' % \
      {
       'site': site,
       'uri': reverse('shout-unsubscribe', 
         kwargs={'slug': object.list.slug}),
      }) 
  m = EmailMessage(
      subject=object.subject,
      body=message,
      from_email=unicode(object.list),
      bcc=bcc, 
      )
  m.send()

def mail_subscription(request, object):
  return mail_member(request, object, 'shout/subscribe_subject.txt',
      'shout/subscribe_message.txt')

def mail_subscription_admin(request, object):
  return mail_admin(request, object, settings.MANAGERS,
      'shout/subscribe_admin_subject.txt', 'shout/subscribe_admin_message.txt')

def mail_unsubscription_admin(request, object):
  return mail_admin(request, object, settings.MANAGERS,
      'shout/unsubscribe_admin_subject.txt', 'shout/unsubscribe_admin_message.txt')
