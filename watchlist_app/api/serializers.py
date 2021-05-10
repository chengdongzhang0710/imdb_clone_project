from rest_framework import serializers
from watchlist_app.models import Review, WatchList, StreamPlatform


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('watchlist', )


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='watch-details')
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
