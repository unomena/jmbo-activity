'''
Created on 09 May 2012

@author: euan
'''
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.decorators import login_required

from activity import views

urlpatterns = patterns('',    
   
    url(r'^my_activity/$',
        login_required(views.MyActivity.as_view(template_name='activity/my_activity.html',
                                                paginate_by=5)),
        name='my-activity'
    ),

    url(r'^my_badges/$',
        login_required(views.MyBadges.as_view(template_name='activity/my_badges.html')),
        name='my-badges'
    ),
    
)