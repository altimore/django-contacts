from django.db import models
from django.db.models import permalink
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from model_utils.models import StatusModel, TimeStampedModel
from model_utils.choices import Choices
from contacts.managers import SpecialDateManager
from autoslug import AutoSlugField

class Company(StatusModel, TimeStampedModel):
	"""Company model."""
	STATUS = Choices(('active', 'Active'), 
					 ('archived', 'Archived'),
					  )
	name = models.CharField(_('name'), max_length=200)
	nickname = models.CharField(_('nickname'), max_length=50, blank=True,
		null=True)
	slug = AutoSlugField(_('slug'), populate_from='name')
	about = models.TextField(_('about'), blank=True, null=True)
	logo = models.ImageField(_('photo'), upload_to='contacts/companies/', blank=True)	

	phone_number = GenericRelation('PhoneNumber')
	email_address = GenericRelation('EmailAddress')
	web_site = GenericRelation('WebSite')
	street_address = GenericRelation('StreetAddress')
	note = GenericRelation(Comment, object_id_field='object_pk')
	

	
	class Meta:
		db_table = 'contacts_companies'
		ordering = ('name',)
		verbose_name = _('company')
		verbose_name_plural = _('companies')
	
	def __unicode__(self):
		return u"%s" % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('contacts_company_update', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})
	
	@permalink
	def get_update_url(self):
		return ('contacts_company_update', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})
	
	@permalink
	def get_delete_url(self):
		return ('contacts_company_delete', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})

class Person(StatusModel, TimeStampedModel):
	"""Person model."""
	STATUS = Choices(('active', 'Active'), 
				 ('archived', 'Archived'),
				  )
	first_name = models.CharField(_('first name'), max_length=100, blank=True, null=True)
	last_name = models.CharField(_('last name'), max_length=200)
	middle_name = models.CharField(_('middle name'), max_length=200, blank=True, null=True)
	suffix = models.CharField(_('suffix'), max_length=50, blank=True, null=True)
	nickname = models.CharField(_('nickname'), max_length=100, blank=True)
	slug = AutoSlugField(_('slug'), populate_from='fullname')
	title = models.CharField(_('title'), max_length=200, blank=True)
	company = models.ForeignKey(Company, blank=True, null=True)
	about = models.TextField(_('about'), blank=True)
	photo = models.ImageField(_('photo'), upload_to='contacts/person/', blank=True)
	
	user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True,
		verbose_name=_('user'))
	
	phone_number = GenericRelation('PhoneNumber')
	email_address = GenericRelation('EmailAddress')
	web_site = GenericRelation('WebSite')
	street_address = GenericRelation('StreetAddress')
	note = GenericRelation(Comment, object_id_field='object_pk')
	

	
	class Meta:
		db_table = 'contacts_people'
		ordering = ('last_name', 'first_name')
		verbose_name = _('person')
		verbose_name_plural = _('people')
	
	def __unicode__(self):
		return (u"%s %s %s" % (self.title, self.first_name, self.last_name)).strip()
	
	@property
	def fullname(self):
		return u"%s %s" % (self.first_name, self.last_name)
	
	@permalink
	def get_absolute_url(self):
		return ('contacts_person_update', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})
	
	@permalink
	def get_update_url(self):
		return ('contacts_person_update', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})
	
	@permalink
	def get_delete_url(self):
		return ('contacts_person_delete', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})

class Group(StatusModel, TimeStampedModel):
	"""Group model."""
	STATUS = Choices(('active', 'Active'), 
                     ('archived', 'Archived'),
                      )
	name = models.CharField(_('name'), max_length=200)
	slug = AutoSlugField(_('slug'), populate_from='name')
	about = models.TextField(_('about'), blank=True)
	
	people = models.ManyToManyField(Person, verbose_name='people', blank=True,
		null=True)
	companies = models.ManyToManyField(Company, verbose_name='companies',
		blank=True, null=True)
	

	
	class Meta:
		db_table = 'contacts_groups'
		ordering = ('name',)
		verbose_name = _('group')
		verbose_name_plural = _('groups')
	
	def __unicode__(self):
		return u"%s" % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('contacts_group_detail', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})
	
	@permalink
	def get_update_url(self):
		return ('contacts_group_update', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})
	
	@permalink
	def get_delete_url(self):
		return ('contacts_group_delete', None, {
		    'pk': self.pk,
			'slug': self.slug,
		})

class Location(StatusModel, TimeStampedModel):
	"""Location model."""
	STATUS = Choices(('active', 'Active'), 
					 ('archived', 'Archived'),
					  )

	WEIGHT_CHOICES = [(i,i) for i in range(11)]
	
	name = models.CharField(_('name'), max_length=200)
	slug = AutoSlugField(_('slug'), populate_from='name')
	is_phone = models.BooleanField(_('is phone'), help_text="Only used for Phone", default=False)
	is_street_address = models.BooleanField(_('is street address'), help_text="Only used for Street Address", default=False)
	
	weight = models.IntegerField(max_length=2, choices=WEIGHT_CHOICES, default=0)
		
	def __unicode__(self):
		return u"%s" % (self.name)
	
	class Meta:
		db_table = 'contacts_locations'
		ordering = ('weight',)
		verbose_name = _('location')
		verbose_name_plural = _('locations')

class PhoneNumber(StatusModel, TimeStampedModel):
	"""Phone Number model."""
	STATUS = Choices(('active', 'Active'), 
					 ('archived', 'Archived'),
					  )
	content_type = models.ForeignKey(ContentType,
		limit_choices_to={'app_label': 'contacts'})
	object_id = models.IntegerField(db_index=True)
	content_object = generic.GenericForeignKey()
	
	phone_number = models.CharField(_('number'), max_length=50)
	location = models.ForeignKey(Location, limit_choices_to={'is_phone': True})
	

	
	def __unicode__(self):
		return u"%s (%s)" % (self.phone_number, self.location)
	
	class Meta:
		db_table = 'contacts_phone_numbers'
		verbose_name = 'phone number'
		verbose_name_plural = 'phone numbers'


class EmailAddress(StatusModel, TimeStampedModel):
	STATUS = Choices(('active', 'Active'), 
					 ('archived', 'Archived'),
					  )
	content_type = models.ForeignKey(ContentType,
		limit_choices_to={'app_label': 'contacts'})
	object_id = models.IntegerField(db_index=True)
	content_object = generic.GenericForeignKey()
	
	email_address = models.EmailField(_('email address'))
	location = models.ForeignKey(Location, limit_choices_to={'is_street_address': False, 'is_phone': False})
	

	def __unicode__(self):
		return u"%s (%s)" % (self.email_address, self.location)
	
	class Meta:
		db_table = 'contacts_email_addresses'
		verbose_name = 'email address'
		verbose_name_plural = 'email addresses'

class WebSite(StatusModel, TimeStampedModel):
	STATUS = Choices(('active', 'Active'), 
					 ('archived', 'Archived'),
					  )
	content_type = models.ForeignKey(ContentType,
		limit_choices_to={'app_label': 'contacts'})
	object_id = models.IntegerField(db_index=True)
	content_object = generic.GenericForeignKey()

	url = models.URLField(_('URL'))
	location = models.ForeignKey(Location, limit_choices_to={'is_street_address': False, 'is_phone': False})


	
	def __unicode__(self):
		return u"%s (%s)" % (self.url, self.location)
	
	class Meta:
		db_table = 'contacts_web_sites'
		verbose_name = _('web site')
		verbose_name_plural = _('web sites')
	
	def get_absolute_url(self):
		return u"%s?web_site=%s" % (self.content_object.get_absolute_url(), self.pk)

class StreetAddress(StatusModel, TimeStampedModel):
	STATUS = Choices(('active', 'Active'), 
					 ('archived', 'Archived'),
					  )
	content_type = models.ForeignKey(ContentType,
		limit_choices_to={'app_label': 'contacts'})
	object_id = models.IntegerField(db_index=True)
	content_object = generic.GenericForeignKey()
	street = models.CharField(_('street'), max_length=100, blank=True)
	street2 = models.CharField(_('street2'), max_length=100, blank=True)
	city = models.CharField(_('city'), max_length=200, blank=True)
	province = models.CharField(_('province'), max_length=200, blank=True)
	postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
	country = models.CharField(_('country'), max_length=100, default="UK")
	location = models.ForeignKey(Location, limit_choices_to={'is_street_address': True})

	
	def __unicode__(self):
		return u"%s, %s %s" % (self.street, self.street2, self.postal_code)
	
	class Meta:
		db_table = 'contacts_street_addresses'
		verbose_name = _('street address')
		verbose_name_plural = _('street addresses')

