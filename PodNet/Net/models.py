#@REF - https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html
#@TODO - able to parse CDATA
#@TODO - parse hit number data per catcher 
#@TODO - parse playlists
#@TODO - ensure podcast name lowercase unique https://stackoverflow.com/questions/7773341/case-insensitive-unique-model-fields-in-django
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

import html
import regex

def tagstr(tag):
  return r"""<{0}[^>]*>([^<]+)<\/{0}>""".format(tag)
TTL=regex.compile(tagstr('title'))
DESC=regex.compile(tagstr('description'))
PUB=regex.compile(tagstr('pubDate'))

import xml.etree.ElementTree as ET
CONTENT_TYPES = (
    ('pod','Podcast'),
    ('yt','YouTube'),
    ('bk','Book'),
    ('nw','News'),#? as own platform?
    ('ar','Article Platform'),#magazines, publishers - 'episode' is article?
    ('vd','VideoFeed'),
    ('lv','Live Show'),
    ('pm','Premium Content'),#maybe not
    ('sm','Social Media'),
    ('al','Album'),

)
class Serial():
  pass
#"Episodic Feed" as base obj for magazines/channels/? "Serial" mixin?
# class productionProcess(models.Model):
  #@TODO Topic object - event in history/news that serves as a common reference point for content or eps
#https://blog.roseman.org.uk/2010/02/15/django-patterns-part-3-efficient-generic-relations/
###MANAGERS 
#https://docs.djangoproject.com/en/2.2/topics/db/managers/#django.db.models.Manager
class PodcastManager(models.Manager):
    def get_queryset(self):
         return super(PodcastManager,self).get_queryset().filter(type='pod')
class YTManager(models.Manager):
    def get_queryset(self):
         return super(YTManager,self).get_queryset().filter(type='yt')
####
class PodCatcher(models.Model):
  pass
class Topic(models.Model):
  pass
  #@TODO - multipart episodes
  #@TODO - generic "relationTemplate" ?
  #@TODO - trim episode description in template
  #@TODO - "Missing Episode"
#@TODO - be able to selectively make content relation not filter upwards?
#@TODO - ordering on categories? - "Primary" etc? - optional?
      # - to account for things like a show that may be funny but isn't necessarily Comedy outright?
#class Checker(models.Model): #periodically rechecks feed, configurable per feed
class CategoryRelation(models.Model):#non-trivial/hierarchical category rels?
  pass
class Category(models.Model):#@TODO case insensitive #@TODO handle subcategories #@TODO handle categories which reference specific content/people/etc? #@TODO 
  parent = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True,blank=True)
  name = models.CharField(max_length=40,unique=True)
  desc = models.TextField(blank=True,null=True)
  def __str__(self):
    return self.name
  def parentPath(self):
    return self.parent
  class Meta:
    verbose_name_plural='Categories'

class Tag(models.Model):#Tags are uses of categories
  cat = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
  class Meta:
    abstract=True#@TODO - unique tag combos


class ContentTag(Tag):
  cont = models.ForeignKey('Content',on_delete=models.SET_NULL,null=True)
class EpisodeTag(Tag):
  ep = models.ForeignKey('Episode',on_delete=models.SET_NULL,null=True)


#@TODO genre vs tag?
# class Warning(models.Model): Trigger/Content Warnings, Explicit tag...
#   pass

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
   lang = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True,blank=True)  
   def __str__(self):
       return self.name
   def FEEDS(self):#@TODO - more reliable way of referencing feeds from pod obj than {{FEEDS.0}}
      feeds=Feed.objects.filter(cont=self)
      return feeds

   def numEps(self):
      return Episode.objects.filter(feed__cont=self).count()
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
#class ParsedFeed(models.Model):#@TODO openblox tower #@TODO person from associated social media accts

FEED_TYPES = [['bs','Basic'],['pm','Premium']]  
#@TODO - "Spinoff Podcast" - rep as child content in a complex?
class Language(models.Model):#@TODO - ability for macrolanguages
    name=models.CharField(max_length=30,null=True)
    iso=models.CharField(max_length=2,null=True)
    def __str__(self):
        return self.name + ' - ['+self.iso+']'
class PodcastNetwork(models.Model): #IS-A Complex?
  pass
class Feed(models.Model):
   # lang #@TODO mixed language per feed/episode?
    #'multi-lingual feed' - assigns language per episode, if not then inherits from feed language 
      #how to account for feeds w like 1/2 translated episodes?
   # @TODO - podcast status
   #@TODO - checkboxes for parse behaviors: 'should make eps', 'should download eps', 'should...'
   # shortname = models.SlugField(blank=True,null=True)
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
   def newestEpisode(self):
      return Episode.objects.filter(feed=self)
   def numEps(self):
      return Episode.objects.filter(feed=self).count()
class Transcript(models.Model):
    transcript_obj=models
class TranscriptWaypoint(models.Model):#@pins transcript (fragment?) to timepoint
  pass
class Episode(models.Model):
  #unique feed/data combo
   feed = models.ForeignKey('Feed',on_delete=models.SET_NULL,null=True)
   epdata = models.TextField(null=True)
   def __str__(self):
       try:
          return self.feed.cont.name+' Episode - '+self.title()
       except:
          return self.title()
   
   def title(self):
    try:
      return TTL.search(self.epdata).group(1)
    except:
      return None
   def description(self):
    try:
      return html.unescape(DESC.search(self.epdata).group(1))
    except:
      return None
   def pubDate(self):
    try:
      return PUB.search(self.epdata).group(1)
    except:
      return None
  #@TODO - file-length, fileurl, itunes attributes (duration, author, explicit, ep icon, keywords,
   class Meta:
      constraints = [models.UniqueConstraint(fields=['feed','epdata'],name="not-doubled")]
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
# class Name(models.Model):#to be able to handle anonymous people? ie names w/o a person object
#   pass
class Name(models.Model):
  pass
class SocialMedia(Platform):
   pass
class SocialMediaProfile(models.Model):
  # person = models.ForeignKey('Person',on_delete=models.SET_NULL,null=True)#@TODO - associate this with content/complex as well? or have two/three diff models?
  url=models.URLField()
  profilee_type = models.ForeignKey(ContentType,on_delete=models.SET_NULL,null=True)#@TODO - "OTHER" category? allowed_types=['person','podcast','youtubechannel','content','complex']
  object_id = models.PositiveIntegerField()#"for_concrete_model'?
  profilee_object = GenericForeignKey('profilee_type','object_id')
  def site(self):
    return self.url.split('://')[1].split('/')[0]
  def __str__(self):
    return self.profilee_object.__str__()+' '+self.profilee_type.__str__()+' profile - '+self.url.__str__()
class Person(models.Model):#Name as its own thing maybe?
   FirstName = models.CharField(max_length=50,blank=True,null=True)
   LastName = models.CharField(max_length=50,blank=True,null=True)
   NickName=models.CharField(max_length=50,blank=True,null=True)
   #must have either First&Last name, or Nick name"
   MiddleName = models.CharField(max_length=50,blank=True)
   Birthday=models.DateField(blank=True,null=True)
   Deathday=models.DateField(blank=True,null=True)

   profiles = GenericRelation(SocialMediaProfile,object_id_field='object_id',content_type_field='profilee_type',related_query_name='profiledperson')
   def __str__(self):
       if self.NickName:
         nickstr=' "{}" '.format(self.NickName)
       else:
         nickstr=" "
       try: 
        return self.FirstName+nickstr+self.LastName
       except:
        return '"{}"'.format(self.NickName)
   class Meta:
       verbose_name_plural = "People"
       constraints = [models.CheckConstraint(check=(models.Q(FirstName__isnull=False) & models.Q(LastName__isnull=False)) | models.Q(NickName__isnull=False),name="Named")]
class FundingPlatform(Platform):
   pass
class Patreon(Website):
   cont = models.ForeignKey('Content',on_delete=models.SET_NULL,null=True)
    
class Guestship(models.Model):
   ep = models.ForeignKey('Episode',on_delete=models.SET_NULL,null=True)
   person = models.ForeignKey('Person',on_delete=models.SET_NULL,null=True)
   def __str__(self):
      return self.person.__str__() + ' guesting '+ self.ep.__str__()
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
class Appearance(models.Model):#shared base obj for host&guest
#@TODO - in-character appearance
#@TODO - episode types - teaser, unlocked
#@TODO - Character - allows for non-named hosts
  pass

class Hostship(models.Model):
    content = models.ForeignKey('Content',on_delete=models.SET_NULL,null=True,blank=True)
    person = models.ForeignKey('Person',on_delete=models.SET_NULL,null=True,blank=True)
    #@TODO - startdate/enddate
    def __str__(self):
      return self.person.__str__() + ' hosting '+ self.content.__str__()
class YoutubeHostship(models.Model):
    channel = models.ForeignKey('YoutubeChannel',on_delete=models.SET_NULL,null=True)
    person = models.ForeignKey('Person',on_delete=models.SET_NULL,null=True)
# class PodcastHostship(Hostship):
#     pass
