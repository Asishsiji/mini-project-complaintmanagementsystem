from django.contrib import admin
from .models import people, complaints
from django.contrib.auth.models import User
# Register your models here.
class peopleAdmin(admin.ModelAdmin):
    list_display = ('user', 'collegename', 'contactnumber', 'type_user', 'Branch',)
    search_fields = ('user__username', 'collegename')
    list_filter = ('type_user', 'Branch')

class complaintsAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'type', 'status', 'date')
    search_fields = ('user__username', 'subject', 'type')
    list_filter = ('status', 'type')

admin.site.register(people, peopleAdmin)
admin.site.register(complaints, complaintsAdmin)

