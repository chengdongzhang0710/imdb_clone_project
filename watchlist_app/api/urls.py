from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (ReviewCreate, ReviewDetail, ReviewList, StreamPlatformVS, WatchListAV,
                                     WatchListDetailsAV)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name='stream-details'),
    path('', include(router.urls)),
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='watch-details'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]
