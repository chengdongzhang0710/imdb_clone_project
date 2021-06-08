from rest_framework import generics, viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from watchlist_app.models import Review, StreamPlatform, Watch
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewerOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle
from watchlist_app.api.pagination import WatchListPagination


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['reviewer__username', 'active']
    search_fields = ['watch__title']
    ordering_fields = ['rating']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watch=pk)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]
    throttle_classes = [ReviewCreateThrottle]

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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(reviewer__username=username)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class WatchVS(viewsets.ModelViewSet):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    permission_classes = [IsAdminOrReadOnly]


class WatchList(generics.ListAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    pagination_class = WatchListPagination
