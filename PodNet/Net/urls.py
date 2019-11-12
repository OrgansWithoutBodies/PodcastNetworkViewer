from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
router.register(r'pods',views.PodcastViewSet)
router.register(r'ppl',views.PersonViewSet)
router.register(r'feeds',views.FeedViewSet)
# router.register(r'podfeeds',views.PodcastFeedViewSet)
router.register(r'eps',views.EpisodeViewSet)
# router.register(r'cats',views.CategoryViewSet)
router.register(r'tagged',views.TaggedContentViewSet)
#@TODO - json access to DRF to populate/order episode lists, queryboxes 

urlpatterns = [
     path('api/',include(router.urls)),
     path('',views.pods,name='base'),
     path('content/<pod_id>',views.content,name="pod_content"),
     	path('content/<pod_id>/&highlight=<highlight_ep_id>',views.content,name="pod_content_highlight"),
     path('category/<cat_id>',views.category,name="category"),
     path('ppl/<person_id>',views.person,name="person"),
     path('content/<pod_id>/get_eps',views.request_eps),
     path('net',views.network_view,name="network")
]