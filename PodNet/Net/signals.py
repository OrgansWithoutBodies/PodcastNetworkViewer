from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from Net import models

import requests
import xml.etree.ElementTree
import datetime
###
#@TODO - parralelize - non-blocking
###
@receiver(post_save,sender=models.Feed)
def retrieveFeed(sender,instance,**kw):
	if should_retrieve(instance):
		feedurl=instance.feedurl
		valurl=is_url_valid(feedurl)

		if valurl:
			models.RetrievedFeed.objects.create(feed=instance,data=valurl.text)
		else:
			print('whoops')
	else:
		pass
		# print('shouldnt retrieve')
	# url_is_feed=True
	# print(feedurl)

@receiver(post_save,sender=models.RetrievedFeed)
def parseFeed(sender,instance,**kw):
	#@TODO - be able to parse atom "next" rels
	try:
		root = xml.etree.ElementTree.fromstring(instance.data)
		channel=root.find('channel')
		if instance.feed.cont is None:
			pod=parse_pod_from_xml(channel)
			instance.feed.cont=pod #@TODO - may get broken if the title changes? idk if this is the best way - triggers feed retrieve, currently shim'd thru retrievePeriod :/
			instance.feed.save()
		# parse_eps_from_xml(channel.findall('item'))
	except:
		raise
		print('nope')
###
def should_retrieve(instance):
	now=datetime.datetime.now()
	try:
		retfeeds=models.RetrievedFeed.objects.filter(feed=instance)
		lastRetrieved=retfeeds.latest('retrievedTimestamp')
		sinceRetrieve=now-lastRetrieved.retrievedTimestamp.replace(tzinfo=None)

		if datetime.timedelta(hours=instance.retrievePeriod)>sinceRetrieve:
			retrieve=False
		else:
			retrieve=True
	except:
		retrieve=True
	return retrieve
def parse_pod_from_xml(channel):
	#sees if there's a pod matching this name, if so set it as the referrent
	title = channel.find('title').text
	# print(title.text)
	matched=models.Podcast.objects.filter(name__iexact=title)
	if len(matched)==0:
		pod = models.Podcast.objects.create(name=title)
	else: #should only b 1 or 0 - @TODO ensure constraint
		pod = matched[0]
	return pod

def parse_eps_from_xml(itemlist):
	[print(item.tag, item.attrib) for item in itemlist]
	subtags = {} #"itunes:","atom:", etc
	#itunes - "duration":"", "author":"author","explicit",'summary','image','subtitle':False,
	#"enclosure":"datafile", "title":"title", "pubDate":"pubDate","description":"shownotes"
def is_url_valid(feedurl):
	try:

		req=requests.get(feedurl,headers={"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})#@TODO configurable headers?
		print(req.status_code)
		valid=True
		return req
	except:
		raise
		valid=False
		return valid

