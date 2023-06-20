import datetime
import requests
import xml.etree.ElementTree

from . import models
from . import tasks
def retrieve_feed(instance):
	feedurl=instance.feedurl
	valurl=is_url_valid(feedurl)

	if valurl:
		models.RetrievedFeed.objects.create(feed=instance,data=valurl.text)
		return True
	else:
		print('whoops')
		return False
def retrieve_feed_if_needed(instance,**kw):
	if should_retrieve(instance):
		return retrieve_feed(instance)
	else:
		print('shouldnt retrieve')
		return False
	# url_is_feed=True
	# print(feedurl)
def get_last_retrieved(instance):
	retfeeds=models.RetrievedFeed.objects.filter(feed=instance)
	return retfeeds.latest('retrievedTimestamp')
def should_retrieve(instance,**kw):
	now=datetime.datetime.now()
	try:
		lastRetrieved=get_last_retrieved(instance)
		sinceRetrieve=now-lastRetrieved.retrievedTimestamp.replace(tzinfo=None)

		if datetime.timedelta(hours=instance.retrievePeriod)>sinceRetrieve:
			retrieve=False
		else:
			retrieve=True
	except:
		retrieve=True
	return retrieve

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


def parse_pod_from_xml(channel):
	#sees if there's a pod matching this name, if so set it as the referrent
	title = channel.find('title').text.strip()
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
def parse_feed(instance,**kw):
	#@TODO - parse thumbnails, render smaller versions
	#@TODO - be able to parse atom "next" rels
	#@TODO - "ShouldParse" attrib
	try:
		root = xml.etree.ElementTree.fromstring(instance.data)
		channel=root.find('channel')
		if instance.feed.cont is None:
			pod=parse_pod_from_xml(channel)
			instance.feed.cont=pod #@TODO - may get broken if the title changes? idk if this is the best way - triggers feed retrieve, currently shim'd thru retrievePeriod :/
			instance.feed.save()

		get_episodes_from_parsed_feed(instance)
		# parse_eps_from_xml(channel.findall('item'))
	except:
		raise
		print('nope')
	
def get_episodes_from_parsed_feed(feedobj):
	#check which eps are new? or leave that to huey
	strfeed=feedobj.data
	# print('sending '+strfeed)
	tsk=tasks.parseEpisodes(strfeed,feedobj)
	tsk()
	###

def dedupe():
	pass