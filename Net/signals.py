from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from Net import models
from Net import tasks

from .utils import *

import requests
import xml.etree.ElementTree
import datetime
###
#@TODO - parralelize - non-blocking
###
@receiver(post_save,sender=models.Feed)
def retrieveFeedIfNeeded(sender,instance,**kw):
	retrieve_feed_if_needed(instance,**kw)


@receiver(post_save,sender=models.RetrievedFeed)
def parseFeed(sender,instance,**kw):
	parse_feed(instance,**kw)