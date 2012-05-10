'''
Created on 07 May 2012

@author: euan
'''
import datetime

from django.db import models
from django.db.models.signals import post_save

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _, ugettext

from photologue.models import ImageModel
from foundry.models import Member
from activity import constants

class PointsActivity(models.Model):
    """The number of points a particular activity earns."""
    
    activity = models.PositiveSmallIntegerField(choices=constants.ACTIVITY_CHOICES, unique=True)
    points = models.PositiveSmallIntegerField()
    limit_per_day = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return '%s = %d points' % (self.get_activity_display(), self.points)
    
    class Meta:
        ordering = ['points']
        verbose_name_plural = 'points activities'

class UserActivity(models.Model):
    """Keeps track of how many, of each kind of activity, the user performs, 
    in order to enforce points limits.
    
    When an instance is saved, it will automatically increment the points
    in the user's profile. When the threshold of the next level is crossed
    it is incremented, and the user notified.

    """
    user = models.ForeignKey(User)
    activity = models.PositiveSmallIntegerField(choices=constants.ACTIVITY_CHOICES)
    sub = models.TextField(null=True, blank=True)
    
    content_content_type = models.ForeignKey(ContentType,
                                             related_name='user_activity_content_object',
                                             null=True, blank=True)
    content_object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_content_type', 'content_object_id')
    
    image_content_type = models.ForeignKey(ContentType,
                                           related_name='user_activity_image_object',
                                           null=True, blank=True)
    image_object_id = models.PositiveIntegerField(null=True, blank=True)
    image_object = generic.GenericForeignKey('image_content_type', 'image_object_id')
    
    points_override = models.PositiveSmallIntegerField(null=True, blank=True)
    over_limit = models.BooleanField(default=False)
    checked_for_badges = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s - %s' % (unicode(self.user), unicode(self.get_activity_display()))
    
    @staticmethod
    def track_activity(user, activity, sub=None, content_object=None, image_object=None, points_override=None):
        from django.contrib.contenttypes.models import ContentType
        from activity.models import UserActivity
        
        kwargs = {'user'  :user, 
                  'activity' : activity,
                  'sub': sub,
                  }
        
        if content_object:
            kwargs.update({'content_content_type' : ContentType.objects.get_for_model(content_object),
                           'content_object_id' : content_object.id
                           })
        
        if image_object:
            kwargs.update({'image_content_type' : ContentType.objects.get_for_model(image_object),
                           'image_object_id' : image_object.id
                           })

        if points_override:
            kwargs.update({'points_override' : points_override})
            
        UserActivity.objects.create(**kwargs)
    
#    @staticmethod
#    def add_gallery(gallery):
#        UserActivity.track_activity(user=gallery.owner,
#                                    activity=ugettext('You added a <a href="%s">Gallery</a>' % gallery.get_absolute_url()),
#                                    sub=gallery.title,
#                                    content_object=gallery,
#                                    image_object=gallery.owner.member)
#    
#    @staticmethod
#    def add_image(image):
#        UserActivity.track_activity(user=image.owner,
#                                    activity=ugettext('You added a <a href="%s">Image</a>' % image.get_absolute_url()),
#                                    sub=image.title,
#                                    content_object=image,
#                                    image_object=image.owner.member)


        
def post_save_user_activity(sender, instance, created, **kwargs):
    """Handler for UserActvity post save."""
    try:
        points_activity = PointsActivity.objects.get(activity=instance.activity)
        if created and instance.user.profile:
            # calculate the points accumulated for activity
            today = datetime.date.today()
            count = UserActivity.objects.filter(
                        user=instance.user,
                        activity=instance.activity,
                        created__range=(today, today + datetime.timedelta(days=1))
                    ).count()
            if count <= points_activity.limit_per_day:
                if instance.points_override:
                    instance.user.profile.as_leaf_class().award_points(instance.points_override)
                else:
                    instance.user.profile.as_leaf_class().award_points(points_activity.points)
            else:
                instance.over_limit = True
                instance.save()
    except PointsActivity.DoesNotExist:
        if instance.points_override:
            instance.user.profile.as_leaf_class().award_points(instance.points_override)

post_save.connect(post_save_user_activity, sender=UserActivity)

def post_save_user(sender, instance, created, **kwargs):
    """Handler for User post save."""
    if created:
        UserActivity.track_activity(instance, constants.ACTIVITY_SIGNED_UP)
    
post_save.connect(post_save_user_activity, sender=UserActivity)

class Badge(ImageModel):
    
    title = models.CharField(max_length=32, unique=True)
    activity = models.PositiveSmallIntegerField(choices=constants.ACTIVITY_CHOICES)
    threshold = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = (('activity', 'threshold'),)
    
    def __str__(self):
        return '%s (%d x %s)' % (self.title,
                                 self.threshold,
                                 self.get_activity_display())
        
class MemberBadge(models.Model):
    member = models.ForeignKey(Member)
    badge = models.ForeignKey(Badge)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('member', 'badge'),)
