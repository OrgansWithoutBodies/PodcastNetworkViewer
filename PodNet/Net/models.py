#@TODO - able to parse CDATA
#@TODO - parse hit number data per catcher 
#@TODO - parse playlists
#@TODO - ensure podcast name lowercase unique https://stackoverflow.com/questions/7773341/case-insensitive-unique-model-fields-in-django
from django.db import models
import xml.etree.ElementTree as ET
CONTENT_TYPES = (
    ('pod','Podcast'),
    ('yt','YouTube'),
    ('bk','Book'),
    ('nw','News'),#? as own platform?
    ('ar','Article'),
    ('lv','Live Show'),
    ('pm','Premium Content'),#maybe not
    ('sm','Social Media'),

)
###MANAGERS 
#https://docs.djangoproject.com/en/2.2/topics/db/managers/#django.db.models.Manager
class PodcastManager(models.Manager):
    def get_queryset(self):
         return super(PodcastManager,self).get_queryset().filter(type='pod')
class YTManager(models.Manager):
    def get_queryset(self):
         return super(YTManager,self).get_queryset().filter(type='yt')
####
# class PodCatcher(models.Model):
#class Checker(models.Model): #periodically rechecks feed, configurable per feed
class Category(models.Model):#@TODO case insensitive #@TODO handle subcategories #@TODO handle categories which reference specific content/people/etc? #@TODO 
  name = models.CharField(max_length=20,unique=True)
  def __str__(self):
    return self.name
  class Meta:
    verbose_name_plural='Categories'

class Tag(models.Model):#Tags are uses of categories
  cat = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
  class Meta:
    abstract=True

class ContentTag(Tag):
  cont = models.ForeignKey('Content',on_delete=models.SET_NULL,null=True)
class EpisodeTag(Tag):
  ep = models.ForeignKey('Episode',on_delete=models.SET_NULL,null=True)




class Complex(models.Model):
   pass
class Platform(models.Model):#@TODO - associate parser(s) w each platform
   pass
class Website(models.Model):
   url = models.URLField()
   class Meta:
       abstract = True 
class Content(models.Model):
   # pass #base class for pods,vids,liveshows,etc 
   name = models.CharField(max_length = 100,null=True)
   type = models.CharField(max_length=4,choices = CONTENT_TYPES,null=True)
   description = models.TextField(blank=True,null=True)
   website = models.URLField(blank = True,null = True)   
   def __str__(self):
       return self.name
class RetrievedFeed(models.Model):#Shouldn't be created manually, gets called by feed on creation and recurrently (somehow)
#@TODO -some way of parsing feed diffs? git-like?
   feed = models.ForeignKey('Feed',blank=True ,on_delete=models.SET_NULL,null=True)
   retrievedTimestamp = models.DateTimeField(auto_now_add=True)
   data=models.TextField(blank=True,null=True)
   def __str__(self):
    return self.feed.__str__()+' - '+self.retrievedTimestamp.strftime('%x %X')
   def treedata(self):#@TODO dict from tree - https://ericscrivner.me/2015/07/python-tip-convert-xml-tree-to-a-dictionary/
     return ET.fromstring(self.data)
   def thumb(self):
      try:
        return self.treedata().find('channel').find('image').find('url').text
      except:
        return ''#@TODO - have "error" thumbnail
   def desc(self):
    try:
      return self.treedata().find('channel').find('description').text
    except:
      return ''
#class ParsedFeed(models.Model):

FEED_TYPES = [['bs','Basic'],['pm','Premium']]  

class Feed(models.Model):
   feedurl = models.URLField(unique=True,null=True)
   feedtype = models.CharField(choices=FEED_TYPES,blank=True,null=True,default='bs',max_length=2)
   cont = models.ForeignKey('Content',blank=True,null=True,on_delete=models.SET_NULL)
   retrievePeriod=models.IntegerField(default='1',help_text='hours')
   def __str__(self):
      if self.cont:
        return self.cont.name
      return self.feedurl
   def lastRetrieved(self):
      retfeeds=RetrievedFeed.objects.filter(feed=self)
      if len(retfeeds)>0:
        return retfeeds.latest('retrievedTimestamp')
      else:
        return None

class Episode(models.Model):
   feed = models.ForeignKey('Feed',on_delete=models.SET_NULL,null=True)

##################
class Podcast(Content):
   objects = PodcastManager()
   def save(self,*args,**kw):
       self.type = 'pod'
       super(Podcast,self).save(*args,**kw)
   def __str__(self):
       return self.name
   class Meta:
       proxy = True
# class VideoFeed(Content):
#   pass
class YoutubeChannel(Content):
   objects = YTManager()
   def __str__(self):
      return self.name
   def save(self,*args,**kw):
      self.type='yt'
      super(YoutubeChannel,self).save(*args,**kw) 
   class Meta:
      proxy=True
class PodcastFeed(models.Model):
   feedurl = models.URLField(unique=True)
   feedname = models.CharField(max_length=50,null=True,blank=True)
   desc = models.TextField(null=True,blank=True)
   thumb = models.URLField(null=True,blank=True)
   pod = models.ForeignKey('Content',on_delete=models.SET_NULL,null=True,blank=True) 
   # def parsedFeed(self):
   #    return 'test'
   def __str__(self):
         if self.feedname:
              return self.feedname
         elif self.pod:
              return self.pod.name
         else:
              return self.feedurl
  
class PodcastEpisode(Episode):
   pass
class YoutubeEpisode(Episode):
   pass
class SubFeed(models.Model): 
   pass
class Person(models.Model):
   FirstName = models.CharField(max_length=50)
   LastName = models.CharField(max_length=50)
   def __str__(self):
       return self.FirstName+" "+self.LastName
   class Meta:
       verbose_name_plural = "People"
class FundingPlatform(Platform):
   pass
class Patreon(Website):
   cont = models.ForeignKey('Content',on_delete="set_null",null=True)
    
class Guestship(models.Model):
   ep = models.ForeignKey('Episode',on_delete=models.SET_NULL,null=True)
   person = models.ForeignKey('Person',on_delete=models.SET_NULL,null=True)
"""
class Speaker(Person):
   pass
class Host(Person):
   pass
class Producer(Person):
   pass
class Owner(models.Model):
   pass
"""
class SocialMedia(Platform):
   pass
class SocialMediaProfile(models.Model):
  person = models.ForeignKey('Person',on_delete="set_null",null=True)#@TODO - associate this with content/complex as well? or have two/three diff models?
  url=models.URLField()
class Hostship(models.Model):
    Content = models.ForeignKey('Content',on_delete="set_null",null=True,blank=True)
    Person = models.ForeignKey('Person',on_delete="set_null",null=True,blank=True)
    #@TODO - startdate/enddate
class YoutubeHostship(models.Model):
    Channel = models.ForeignKey('YoutubeChannel',on_delete="set_null",null=True)
    Person = models.ForeignKey('Person',on_delete="set_null",null=True)
# class PodcastHostship(Hostship):
#     pass
class Name(models.Model):
    pass
