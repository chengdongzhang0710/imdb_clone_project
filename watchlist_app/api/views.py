from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from watchlist_app.models import Review, StreamPlatform, Watch
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewerOrReadOnly


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watch=pk)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watch = Watch.objects.get(pk=pk)
        reviewer = self.request.user
        queryset = Review.objects.filter(watch=watch, reviewer=reviewer)
        if queryset.exists():
            raise ValidationError('You have already reviewed this watch!')
        if watch.number_rating == 0:
            watch.avg_rating = serializer.validated_data['rating']
        else:
            watch.avg_rating = (watch.avg_rating * watch.number_rating +
                                serializer.validated_data['rating']) / (watch.number_rating + 1)
        watch.number_rating += 1
        watch.save()
        serializer.save(watch=watch, reviewer=reviewer)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class WatchVS(viewsets.ModelViewSet):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
