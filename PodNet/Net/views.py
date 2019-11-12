from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.utils import encoding
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from .models import *
from .viewsets import *
from .utils import *

from . import tasks
from . import hvs
CACHE={}
#FEEDS ,
#@TODO - "in_bulk()"
#@TODO - launch by 300
#@TODO parse social media links in description
#@TODO - if playing a character of a real person, then can credit appearance of name but not person
#@TODO - some way of attributing clips from other sources
#@TODO "Crossover Ep" - auto suggests hosts from both shows as appearances,
#@TODO - 'reaired ep'
#@TODO - "Crosspost" - same episode in multiple feeds 
#@TODO - "debug mode" which shows certain ids & such
#@TODO - partial escape of links/format changes?
		#limit image size
#@TODO - fix lingering unicode issues \xe3 etc - chardet? - https://www.youtube.com/watch?v=sgHbC6udIqc
#@TODO - \n
#@TODO - deal with "the", "a", "an", etc
#@TODO - # of episodes to return
#@TODO - obscure PK's
#@TODO - choosers 
#			feeds - language, categories, last-published-episode, min # eps
#			eps - host/guested by, length cluster, topic category
#@TODO - orderers
		#	feeds - published date, alphabetical (w/wo number?), length, # eps
def cache(pod):
  if pod in CACHE.keys():
       print(CACHE)
       return CACHE[pod] 

def buildNetwork():
  pass
def person(request,person_id):
	prsn=Person.objects.get(pk=person_id)
	hosts=Hostship.objects.filter(person=prsn)
	guests=Guestship.objects.filter(person=prsn)
	socmed=SocialMediaProfile.objects.filter(Q(profilee_type=ContentType.objects.get_for_model(Person))&Q(object_id=person_id))
	context={'person':prsn,'hosts':hosts,'guests':guests,'socs':socmed}
	return TemplateResponse(request,'Net/person.html',context)
def pods(request): 
    #@TODO - deal with "the"
    #@TODO - caching
    #@TODO - make faster/preloaded dealing w/ filters

    context = {'pods':Feed.objects.filter(cont__isnull=False)}
    return TemplateResponse(request,'Net/pods.html',context) 
def category(request,cat_id=None):
	cat=Category.objects.get(pk=cat_id)
	cont_tags=ContentTag.objects.filter(cat=cat)
	ep_tags=EpisodeTag.objects.filter(cat=cat)
	context={'cat':cat,'cont':cont_tags,'eps':ep_tags}
	return TemplateResponse(request,'Net/category.html',context)
def content(request,pod_id,highlight_ep_id=None):
	if highlight_ep_id is not None:
		
		highlight_ep_id	= int(highlight_ep_id)
	pod=Feed.objects.get(pk=pod_id)
	eps=Episode.objects.filter(feed=pod)
	hosts=Hostship.objects.filter(content_id=pod.cont)
	tags=ContentTag.objects.filter(cont=pod.cont)
	guestships=Guestship.objects.filter(ep__feed__cont=pod.cont)
	_guests={g['person_id'] for g in guestships.values()}
	guests=[Person.objects.get(pk=g) for g in _guests]
	# guests=guestships.distinct()#distinct('person') only works w postgres
	# print(test)
	# guests=Person.objects.filter(guestship__ep__feed__cont=pod.cont).distinct()#@TODO - count of guest appearances,
	#@TODO guestships & guest person as two different vars? guestships for ft per episode item, while person to acct for distincts on pod_info?
	context = {'pod':pod,'eps':eps,'hosts':hosts,'guests':guests,'tags':tags,'highlight_ep':highlight_ep_id}
	return TemplateResponse(request,'Net/pod_info.html',context)

def request_eps(request,pod_id):
	pod=Feed.objects.get(pk=pod_id)
	stat=retrieve_feed(pod)
	return JsonResponse({'status':stat})	
def network_view(request):
	CATS=Category.objects.all()
	CATPARENTS = {C:Category.objects.filter(parent=C) for C in Category.objects.filter(Q(parent__isnull=True) & Q(category__isnull=False))} #@TODO able to query entire child tree in one query
	PODCATS={C:[Podcast.objects.filter(Q(contenttag__cat=C)),Episode.objects.filter(Q(episodetag__cat=C))] for C in CATS} #@TODO contenttag & episodetag on one query
	PERSONAPPS={P:[Hostship.objects.filter(Q(person=P)),Guestship.objects.filter(Q(person=P))] for P in Person.objects.filter(Q(hostship__isnull=False)|Q(guestship__isnull=False))}
	PODAPPS={P:[Hostship.objects.filter(Q(content=P)),Guestship.objects.filter(Q(ep__feed__cont=P))] for P in Podcast.objects.filter(Q(hostship__isnull=False))}

	HOSTEDGEBASE={
				p.name:set(
					pp for pp in p.hostship_set.values_list('person__hostship__content__name',flat=True) if pp!=p.name
					) for p in PODAPPS.keys()}#if there's a common host, share an edge type 0 - if there's a common person who has been both a guest &/or a host (any type of appearance) then share an edge of type 1
					#FOR ALL HOSTS IN POD.HOSTSHIP_SET GET HOST.CONTENT_SET
	# print(APPEDGEBASE)
	GUESTHOSTEDGEBASE={p.name:[
						hst.person.guestship_set.values_list('ep__feed__cont__name',flat=True) for hst in p.hostship_set.all() if (hst.person.guestship_set.count()>0)
					] for p in PODAPPS.keys()}#gets all hosts who have been guests

	GUESTHOSTEDGESET=[{a,aaa} for a in GUESTHOSTEDGEBASE for aa in GUESTHOSTEDGEBASE[a] for aaa in aa]
	# print(GUESTHOSTEDGES)
	APPEDGES=[[frozenset([a,aa]) for aa in HOSTEDGEBASE[a]] for a in HOSTEDGEBASE.keys() if HOSTEDGEBASE[a]!=set()]
	APPEDGESSET=set([aa for a in APPEDGES for aa in a])

	# netview=hvs.networkView(CATPARENTS,[])
	netview=hvs.networkView(PODAPPS,[[APPEDGESSET,{'color':'black'}],[GUESTHOSTEDGESET,{"color":'red'}]],hvs.podappearancenetwork)
	# netview=hvs.networkView(PODCATS)
	context={'PC':PODCATS,'HG':PERSONAPPS,'CP':CATPARENTS,'nv':netview}
	return TemplateResponse(request,"Net/network.html",context)
def network_data(request):
	#get all podcasts tagged w each category
	context={}
	return JsonResponse(context)
def bokeh_server_status():
	return False
	#@TODO - add salt to grocy