from django.contrib import admin
from .models import Realtor

# Register your models here.
class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','date_hired')
    list_display_links =('id', 'name')
    search_fields= ('name',)

admin.site.register(Realtor, RealtorAdmin)