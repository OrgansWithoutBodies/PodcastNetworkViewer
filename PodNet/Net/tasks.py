from huey.contrib.djhuey import periodic_task, task
import xml.etree.ElementTree as ETree
from Net import models 

@task()
def parseEpisodes(parsedFeed,feedObj):
    parser=ETree.XMLParser(encoding='UTF-8')
    root=ETree.fromstring(parsedFeed,parser=parser)

    eps=root.find('channel').findall('item')
    print('adding {} episodes...'.format(len(eps)))
    for ep in eps:
        models.Episode.objects.create(epdata=ETree.tostring(ep,encoding="utf-8"),feed=feedObj.feed)
    #find things with label "items", make an episode object w it in it
    #base: title, link, pubDate, description, enclosure
    #itunes - image, explicit, subtitle, author, summary, duration

@task()
def retrieveFeed(feedURL):
    print(feedURL)
