from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework import viewsets

from .models import *
from .serializers import *
CACHE={}
def cache(pod):
  if pod in CACHE.keys():
       print(CACHE)
       return CACHE[pod] 
class PodcastViewSet(viewsets.ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
class PodcastFeedViewSet(viewsets.ModelViewSet):
    queryset = PodcastFeed.objects.all()
    serializer_class = PodcastFeedSerializer
def pods(request): 
    #@TODO - deal with "the"
    #@TODO - make faster/preloaded dealing w/ filters
    context = {'pods':PodcastFeed.objects.all()}
    return TemplateResponse(request,'Net/pods.html',context) 