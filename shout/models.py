# vim: set fileencoding=utf-8 :

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site

class List(models.Model):
  """Represents a list of people that would like to receive announcements"""

  class Meta:
    permissions = ( 
         ('view_list', 'Can view list'), 
         ('email_list', 'Can email to list'), 
                  )

  def __unicode__(self):
    site = Site.objects.get_current()
    return u'%(name)s <%(slug)s@%(site)s>' % \
        {'name':self.name, 'slug': self.slug, 'site': site.domain.split(':')[0]}

  name = models.CharField(_(u'Name'), max_length=256, help_text=_(u'The name of your announcement list'), null=False, blank=False)
  slug = models.SlugField(_(u'Slug'), max_length=64, help_text=_(u'A shorter, slug entry so I can fake e-mails From fields.'), null=False, blank=False, unique=True)
  creation = models.DateTimeField(_(u'Creation'), help_text=_(u'Set here the creation date of your list.'), editable=False, auto_now_add=True)

class Member(models.Model):
  """A person that subscribes to the announcement list"""

  class Meta:
    unique_together = (
          ('email', 'list'),
        )

  def __unicode__(self):
    if self.mobile:
      return u'%(name)s (%(mobile)s) <%(email)s>' % \
          {'name': self.name, 'email': self.email, 'mobile': self.mobile} 
    else:
      return u'%(name)s <%(email)s>' % \
          {'name': self.name, 'email': self.email} 

  name = models.CharField(_(u'Name'), max_length=256, help_text=_(u'Your complete name'), null=False, blank=False)
  email = models.EmailField(_(u'E-mail'), max_length=256, help_text=_(u'Your e-mail'), null=False, blank=False)
  mobile = models.CharField(_(u'Mobile phone number'), max_length=64, help_text=_(u'Your mobile phone number in the format +417X1234567, if you would like to receive SMSs'), null=True, blank=True)
  joined = models.DateTimeField(_(u'Joined'), help_text=_(u'Set here the joining date of this member.'), null=False, blank=False, auto_now_add=True)
  list = models.ForeignKey(List, help_text=_(u'Choose the list this member wants to be associated to'))
  language = models.CharField(_(u'Language'), max_length=6, help_text=_(u'Choose your preferred language. This setting will be used primarily for automatically generated messages.'), null=False, blank=False, default='fr', choices=settings.LANGUAGES)

class Message(models.Model):
  """A message that was sent to a certain list"""

  subject = models.CharField(_(u'Subject'), max_length=256, help_text=_(u'The subject of your message'), null=False, blank=False)
  message = models.TextField(_(u'Message'), help_text=_(u'The body of the message'), null=False, blank=False)
  list = models.ForeignKey(List, help_text=_(u'Choose the list this member wants to be associated to'))
  sent = models.DateTimeField(_(u'Sent'), help_text=_(u'Set here the date of this message.'), null=False, blank=False, auto_now_add=True)
  by = models.ForeignKey(User, help_text=_('The site user that has sent the message'), blank=False, null=False, related_name='message_sender')
