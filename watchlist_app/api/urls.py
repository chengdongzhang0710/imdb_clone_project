from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (ReviewCreate, ReviewDetail, ReviewList, StreamPlatformVS, UserReview, WatchList,
                                     WatchVS)

router = DefaultRouter()
router.register('list', WatchVS, basename='watch')
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('review/', UserReview.as_view(), name='user-review'),
    path('all/', WatchList.as_view(), name='watch-all'),
]
