from django.contrib import admin

from suite.models import *

# Register your models here.
class TestModelAdmin(admin.ModelAdmin):
	pass

admin.site.register(TestModel, TestModelAdmin)
