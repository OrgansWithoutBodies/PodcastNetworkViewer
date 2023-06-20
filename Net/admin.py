from django.contrib import admin
from django.forms import widgets
from django import forms
from django.contrib.contenttypes.admin import GenericStackedInline,GenericTabularInline
from .models import * 
#
TAGS = {"@":Person,"#":Topic,"$":Content,"_":Episode} #checks if prefix matches, if so return matches w/in matching api obj
class QueryBoxWidget(widgets.TextInput):#@TODO flexible based on # of fields, ...
    # def __init__(self,*arg,**kw):
    #     # kw['attrs']={'class':'query'}
    #     print(arg,kw)        
    #     super(widgets.TextInput,self).__init__(*arg,**kw)

    @property
    def media(self):
        return forms.Media(js=('admin/adminfns.js',),css={'all':('admin/admin.css',)})
    
    # def get_context(self,name,value,attrs):
    #     print(attrs)
    #     super(widgets.TextInput,self).get_context(name,value,attrs)

class Suggester():#suggesting parsed results/suggestions from Neural Net
    pass
#@TODO - admin button to refresh all feeds
#@TODO categoryQuery allows reference to other items
#@TODO querybox suggests hosts for appearances on episodes
#@TODO - 0 inlines before related to other object http://www.joshuakehn.com/2014/10/19/fixing-djangos-admin-inlines.html
class ContentTagInline(admin.StackedInline):
    model=ContentTag
class EpisodeTagInline(admin.StackedInline):
    model=EpisodeTag

class HostshipInline(admin.TabularInline):
     model = Hostship
     extra = 2
class GuestshipInline(admin.TabularInline):#@TODO - be able to handle large db's - limit # in dropdown ( https://stackoverflow.com/questions/15074138/django-admin-inline-queryset-limit ), include querybox ( https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_foreignkey )
    model = Guestship
    extra = 2
class SocialMediaProfileInline(GenericTabularInline):
    model = SocialMediaProfile 
    ct_field='profilee_type'
    ct_fk_field='object_id'
    extra = 1
class FeedInline(admin.TabularInline):
    model = Feed
    extra=0
class EpisodeInline(admin.TabularInline):
    model=Episode
###

class AddPodForm(forms.ModelForm):

    class Meta:
        model = Feed
        widgets = {
            'cont':QueryBoxWidget(attrs={'class':'query','autocomplete':'off'}),
        }
        fields="__all__"


@admin.register(Podcast,YoutubeChannel)
class ContentAdmin(admin.ModelAdmin):
    exclude = ('type',)
    list_display=('__str__','numEps',)
    inlines = [HostshipInline,FeedInline,ContentTagInline,SocialMediaProfileInline]

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    inlines=[EpisodeInline]
    list_display = ('__str__','numEps',)
    form = AddPodForm
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_per_page=2000
    inlines = [GuestshipInline,EpisodeTagInline]
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fieldsets = (('Required',{'fields':['FirstName','NickName','LastName']}),('Detailed',{'fields':['MiddleName','Birthday','Deathday'],'classes':('collapse',)}))
    # inlines=[HostshipInline,GuestshipInline,SocialMediaProfileInline]
    inlines=[SocialMediaProfileInline,HostshipInline]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ContentTagInline]

@admin.register(SocialMediaProfile)
class SocialMediaProfileAdmin(admin.ModelAdmin):
    class Meta:
        fields='__all__'
    # inlines=[GenericStackedInline()]
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
admin.site.register(EpisodeTag)
admin.site.register(Language)
# admin.site.register
# admin.site.register(SocialMediaProfile)
# admin.site.register(Category)
# admin.site.register(PodcastFeed)
# admin.site.register(Guestship)
