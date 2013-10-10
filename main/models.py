
from time import time
from datetime import datetime
from urlparse import urlparse

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.core.models import Displayable, Ownable
from mezzanine.generic.models import Rating
from mezzanine.generic.fields import RatingField, CommentsField

# from mezzanine.core.managers import SearchableManager


class Link(Displayable, Ownable):

    link = models.URLField()
    rating = RatingField()
    comments = CommentsField()
    
    # objects = SearchableManager()
    # search_fields = ("title", "description")

    @models.permalink
    def get_absolute_url(self):
        return ("link_detail", (), {"slug": self.slug})

    def domain(self):
        return urlparse(self.link).netloc


class Profile(models.Model):

    user = models.OneToOneField("auth.User")
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    karma = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        return "%s (%s)" % (self.user, self.karma)


@receiver(post_save, sender=Rating)
def karma(sender, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2.
    """
    rating = kwargs["instance"]
    value = int(rating.value)
    if not kwargs["created"]:
        value *= 2
    content_object = rating.content_object
    if rating.user != content_object.user:
        queryset = Profile.objects.filter(user=content_object.user)
        queryset.update(karma=models.F("karma") + value)











# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example
# from django.db import models
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )
# 
# 
# class ProfileManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
# 
#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#         )
# 
#         user.set_unusable_password(password)
#         user.save(using=self._db)
#         return user
# 
#     def create_superuser(self, email, date_of_birth, password):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(email,
#             password=password
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
# 
# 
# class Profile(AbstractBaseUser):
#     email = models.EmailField(
#                         verbose_name='email address',
#                         max_length=255
#                     )
#     user = models.OneToOneField("auth.User")
#     website = models.URLField(blank=True)
#     bio = models.TextField(blank=True)
#     karma = models.IntegerField(default=0, editable=False)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     
#     objects = ProfileManager()
#     
#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['date_of_birth']
#     
#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email
# 
#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email
# 
#     # On Python 3: def __str__(self):
#     def __unicode__(self):
#         return self.email
# 
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
# 
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
# 
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
# 
#     def __unicode__(self):
#         return "%s (%s)" % (self.user, self.karma)