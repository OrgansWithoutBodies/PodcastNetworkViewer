from django.db import models
CONTENT_TYPES = (
    ('pod','Podcast'),
    ('yt','YouTube'),
    ('lv','Live Show'),
    ('pm','Premium Content'),#maybe not
    ('sm','Social Media'),

)
class PodcastManager(models.Manager):
    def get_queryset(self):
         return super(PodcastManager,self).get_queryset().filter(type='pod')
class YTManager(models.Manager):
    def get_queryset(self):
         return super(YTManager,self).get_queryset().filter(type='yt')
class Complex(models.Model):
   pass
class Platform(models.Model):
   pass
class Website(models.Model):
   url = models.URLField()
   class Meta:
       abstract = True 
class Content(models.Model):
   pass #base class for pods,vids,liveshows,etc 
   name = models.CharField(max_length = 100,null=True)
   type = models.CharField(max_length=4,choices = CONTENT_TYPES,null=True)
   description = models.TextField(blank=True,null=True)
   website = models.URLField(blank = True,null = True)   
   def __str__(self):
       return self.name
class Feed(models.Model):
   pass
class Episode(models.Model):
   pass
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
   pod = models.ForeignKey('Content',on_delete='set_null',null=True,blank=True) 
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
    
"""
class Guest(Person):
   pass
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
class Hostship(models.Model):
    Content = models.ForeignKey('Content',on_delete="set_null",null=True,blank=True)
    Person = models.ForeignKey('Person',on_delete="set_null",null=True,blank=True)

class YoutubeHostship(models.Model):
    Channel = models.ForeignKey('YoutubeChannel',on_delete="set_null",null=True)
    Person = models.ForeignKey('Person',on_delete="set_null",null=True)
class PodcastHostship(Hostship):
    pass
class Name(models.Model):
    pass
