from rest_framework import serializers
from .models import * 
class CategorySerializer(serializers.ModelSerializer):
    # EpisodeTags = serializers.RelatedField(source='EpisodeTag.ep',read_only=True)
    # ContentTags = serializers.RelatedField(source='ContentTag.cont',read_only=True)
    # ContentTags=serializers.StringRelatedField(many=True)
    class Meta:
       model = Category
       fields = ['name',]

       depth=1
class ContentTagSerializer(serializers.ModelSerializer):
  class Meta:
    depth=1
    model = ContentTag
    fields=['cat',]
  cat = CategorySerializer()
class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        # depth=2
        model = Podcast
        fields = ['__str__','numEps','lang','contenttag_set']
    contenttag_set=ContentTagSerializer(many=True)
class FeedSerializer(serializers.ModelSerializer):
    class Meta:
       model = Feed
       depth=1
       fields = ['feedurl','cont']
    # cont=PodcastSerializer()
class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
       model = Episode
       fields = ['feed','title','pubDate','description']
    feed = FeedSerializer()
class HostshipSerializer(serializers.ModelSerializer):
  class Meta:
    model=Hostship
    fields=['content',]
    depth=1
  # content = PodcastSerializer()
class GuestshipSerializer(serializers.ModelSerializer):
  class Meta:
    model=Hostship
    fields=['ep',]
  ep = EpisodeSerializer()
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        depth=2
        model = Person
        fields = ['__str__','guestship_set','hostship_set']
    hostship_set=HostshipSerializer(many=True)
    guestship_set=GuestshipSerializer(many=True)


# class PodcastFeedSerializer(serializers.ModelSerializer):
#     class Meta:
#        model = PodcastFeed
#        fields = '__all__'



class TaggedContentSerializer(serializers.ModelSerializer):
  class Meta:
       model = Category
       fields = ['name','contenttag_set','episodetag_set']
       depth=2

#@TODO - custom serializer class which allows hiding 