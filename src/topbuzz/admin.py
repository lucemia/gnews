from django.contrib import admin
from .models import Stat, Channel

# Register your models here.

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', )


class StatAdmin(admin.ModelAdmin):
    list_display = ('channel', 'date', 'recommend', 'read')
    list_filter = ('channel', )
    date_hierarchy = 'date'


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Stat, StatAdmin)
