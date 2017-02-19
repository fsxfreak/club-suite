from django.contrib import admin

from suite.models import *

# Register your models here.

# mdl_user.py
class UserAdmin(admin.ModelAdmin):
   pass

admin.site.register(User, UserAdmin)

class AccountAdmin(admin.ModelAdmin):
   pass

admin.site.register(Account, AccountAdmin)

#mdl_club.py
class ClubAdmin(admin.ModelAdmin):
   pass

admin.site.register(Club, ClubAdmin)

#mdl_event.py
class EventAdmin(admin.ModelAdmin):
   pass

admin.site.register(Event, EventAdmin)
