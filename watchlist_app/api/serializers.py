from rest_framework import serializers
from watchlist_app.models import Review, Watch, StreamPlatform


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('watch', )


class WatchSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Watch
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    watch = WatchSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
