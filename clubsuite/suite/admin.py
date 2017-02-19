from django.contrib import admin

from suite.models import *
# Register your models here.
#class TestModelAdmin(admin.ModelAdmin):
#	pass

#admin.site.register(TestModel, TestModelAdmin)

# user
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

# account
class AccountAdmin(admin.ModelAdmin):
    pass

admin.site.register(Account, AccountAdmin)

# club
class ClubAdmin(admin.ModelAdmin):
    pass

admin.site.register(Club, ClubAdmin)

# event
class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)

# receipt
class ReceiptAdmin(admin.ModelAdmin):
    pass

admin.site.register(Receipt, ReceiptAdmin)

# budget
class BudgetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Budget, BudgetAdmin)

# role
class RoleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Role, RoleAdmin)

# division
class DivisionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Division, DivisionAdmin)

# event_sign_in
class EventSignInAdmin(admin.ModelAdmin):
    pass

admin.site.register(EventSignIn, EventSignInAdmin)
