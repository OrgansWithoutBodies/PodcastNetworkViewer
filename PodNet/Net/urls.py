from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
router.register(r'pods',views.PodcastViewSet)
router.register(r'podfeeds',views.PodcastFeedViewSet)
urlpatterns = [
     path('api/',include(router.urls)),
     path('',views.pods)
]
