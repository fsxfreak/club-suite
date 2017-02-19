from django.contrib import admin

from suite.models import *

class UserModelAdmin(admin.ModelAdmin):
	pass

admin.site.register(User, UserModelAdmin)
