from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes,schema
from rest_framework.schemas import AutoSchema
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import *

class PodcastViewSet(viewsets.ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    permission_classes=[IsAuthenticated]
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes=[IsAuthenticated]
# class PodcastFeedViewSet(viewsets.ModelViewSet):
#     queryset = PodcastFeed.objects.all()
#     serializer_class = PodcastFeedSerializer
class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes=[IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[IsAuthenticated]
class TaggedContentViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = TaggedContentSerializer
    permission_classes=[IsAuthenticated]


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset=Episode.objects.all()
    serializer_class=EpisodeSerializer
    pagination_class=LimitOffsetPagination
    permission_classes=[IsAuthenticated]
    # def list(self,request):
    #   queryset=self.get_queryset()
    #   serializer=self.serializer_class(queryset,many=True)
    # #   return Response(serializer.data)
    # def get(self,request,blog_id=None,*args,**kw):
    #     # content=parsePOST(request,PostSerializer)
    #     return self.list(request,*args,**kw)
    #     # return self.list([p.id for p in Post.objects.all()])


    # def post(self,request,*args,**kw):
    #     return self.create(request,*args,**kw)
    #   if blog_id:
    #       content={'posts':PostSerializer(Post.objects.filter(blog_id=blog_id),many=True).data}
    #   else:
    #       content = {'posts':PostSerializer(Post.objects.all(),many=True).data}
    #   return Response(content)
