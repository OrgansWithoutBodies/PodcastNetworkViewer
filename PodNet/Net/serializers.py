from rest_framework import serializers
from .models import * 

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'


class PodcastFeedSerializer(serializers.ModelSerializer):
    class Meta:
       model = PodcastFeed
       fields = '__all__'

