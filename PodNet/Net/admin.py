from django.contrib import admin
from .models import * 
#@TODO - admin button to refresh all feeds
class ContentTagInline(admin.StackedInline):
	model=ContentTag
class HostshipInline(admin.TabularInline):
     model = Hostship
     extra = 2
class GuestshipInline(admin.TabularInline):
	model = Guestship
	extra = 2
class SocialMediaProfileInline(admin.TabularInline):
	model = SocialMediaProfile 
	extra = 1
class FeedInline(admin.TabularInline):
	model = Feed
	extra=0
class EpisodeInline(admin.TabularInline):
	model=Episode
###
@admin.register(Podcast,YoutubeChannel)
class ContentAdmin(admin.ModelAdmin):
    exclude = ('type',)
    inlines = [HostshipInline,FeedInline,ContentTagInline]

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
	inlines=[EpisodeInline]
	# fields = (,)
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
	inlines = [GuestshipInline,]
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	inlines=[HostshipInline,GuestshipInline,SocialMediaProfileInline]
# @admin.register(Podcast)
# class PodcastAdmin(ContentAdmin):
#     inlines = [   
#     ]
# @admin.register(YoutubeChannel)
# class YTChannelAdmin(ContentAdmin):
#      inlines = [
#      ]
###
admin.site.register(RetrievedFeed)
admin.site.register(Category)
# admin.site.register(PodcastFeed)
# admin.site.register(Hostship)
