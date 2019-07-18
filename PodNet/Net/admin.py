from django.contrib import admin
from .models import * 

class HostshipInline(admin.TabularInline):
     model = Hostship

class ContentAdmin(admin.ModelAdmin):
    exclude = ('type',)

@admin.register(Podcast)
class PodcastAdmin(ContentAdmin):
    inlines = [
        HostshipInline,
    ]

class YTHostshipInline(admin.TabularInline):
     model = YoutubeHostship

@admin.register(YoutubeChannel)
class YTChannelAdmin(ContentAdmin):
     inlines = [
          HostshipInline,
     ]

admin.site.register(PodcastFeed)
admin.site.register(Person)
admin.site.register(Hostship)
