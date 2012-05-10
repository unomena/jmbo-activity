'''
Created on 08 Apr 2012

@author: euan
'''
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _, ugettext

from foundry import models as foundry_models
from activity import constants, models

class Command(BaseCommand):
    """
    Calculates and awards badges to members
    """
    def handle(self, *args, **options):
        # Get the latest activities - we assume the site is busy, so we'll only look at the new ones.
        latest_activities = models.UserActivity.objects.filter(checked_for_badges=False)
        # Only need to check active users - ignore the inactive ones for now.
        for member in foundry_models.Member.objects.filter(pk__in=[activity.user.id for activity in latest_activities]):
            for activity in dict(constants.ACTIVITY_CHOICES).keys():
                # Step through all the badges a user is entitled to.
                for badge in models.Badge.objects.filter(activity=activity, 
                    threshold__lte=member.useractivity_set.filter(activity=activity).count()):
                    # Award member new badge, if not already in possession of it.
                    member_badge, created = models.MemberBadge.objects.get_or_create(member=member, 
                                                                                     badge=badge)
                    if created:
                        link, dc = foundry_models.Link.objects.get_or_create(
                            title=ugettext("You have earned a new badge"), view_name='my-badges'
                        )
                        foundry_models.Notification.objects.get_or_create(member=member, link=link)
        
        # Mark them, so we don't have to check them again.
        latest_activities.update(checked_for_badges=True)