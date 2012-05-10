'''
Created on 09 May 2012

@author: euan
'''
from django.views.generic import ListView, TemplateView

from foundry import models as foundry_models
from activity import constants, models

class MyActivity(ListView):
    
    def get_queryset(self):
        return self.request.user.useractivity_set.all().order_by('-created')

class MyBadges(ListView):
    
    def get_queryset(self):
        print self.request.user.member.memberbadge_set.all().order_by('-created')
        return self.request.user.member.memberbadge_set.all().order_by('-created')
    
    
class BadgeGroup:
    title = None
    badges = []
    
class MyBadges(TemplateView):
    
    def get_context_data(self, **kwargs):
        
        badge_groups = []
        for activity in dict(constants.ACTIVITY_CHOICES).keys():
            badge_group = BadgeGroup()
            badge_group.title = dict(constants.ACTIVITY_CHOICES)[activity]
            badge_group.badges = []

            for badge in models.Badge.objects.filter(activity=activity):
                if models.MemberBadge.objects.filter(member=self.request.user.member, badge=badge).count() == 1:
                    badge.is_awarded = True
                
                badge_group.badges.append(badge)
            
            if len(badge_group.badges) > 0:
                badge_groups.append(badge_group)

        link, dc = foundry_models.Link.objects.get_or_create(
            title='You have been awarded a new badge.', view_name='my-badges'
        )
        foundry_models.Notification.objects.filter(member=self.request.user.member, link=link).delete()

        return { 'badge_groups' : badge_groups }
    