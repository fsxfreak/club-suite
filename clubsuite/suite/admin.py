from django.contrib import admin

from suite.models import *

# Register your models here.
class TestModelAdmin(admin.ModelAdmin):
	pass

admin.site.register(TestModel, TestModelAdmin)

# mld_user.py
class UserAdmin(admin.ModelAdmin):
   pass

admin.site.register(User, UserAdmin)

class AccountAdmin(admin.ModelAdmin):
   pass

admin.site.register(Account, AccountAdmin)
