from rest_framework import serializers
from watchlist_app.models import Review, Watch, StreamPlatform


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watch', )


class WatchSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = Watch
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    watch = WatchSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
