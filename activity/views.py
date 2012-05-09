'''
Created on 09 May 2012

@author: euan
'''
from django.views.generic import ListView

class MyActivity(ListView):
    
    def get_queryset(self):
        return self.request.user.useractivity_set.all().order_by('-created')

class MyBadges(ListView):
    
    def get_queryset(self):
        return self.request.user.member.memberbadge_set.all().order_by('-created')