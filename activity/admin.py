from django.contrib import admin

from activity import models

admin.site.register(models.PointsActivity)
admin.site.register(models.UserActivity)
admin.site.register(models.BadgeGreyImage)
admin.site.register(models.Badge)
admin.site.register(models.MemberBadge)