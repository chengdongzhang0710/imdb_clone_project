# from django.shortcuts import get_object_or_404
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from watchlist_app.models import Review, StreamPlatform, WatchList
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchListSerializer


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watch = WatchList.objects.get(pk=pk)
        serializer.save(watchlist=watch)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         queryset = StreamPlatform.objects.all()
#         watch = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watch)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def update(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def destory(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class StreamPlatformAV(APIView):
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many=True)
#         # serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class StreamPlatformDetailsAV(APIView):
#     def get(self, request, pk):
#         try:
#             stream = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Error': 'Stream not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(stream)
#         # serializer = StreamPlatformSerializer(stream, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    def get(self, request):
        watches = WatchList.objects.all()
        serializer = WatchListSerializer(watches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetailsAV(APIView):
    def get(self, request, pk):
        try:
            watch = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Watch not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watch)
        return Response(serializer.data)

    def put(self, request, pk):
        watch = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        watch = WatchList.objects.get(pk=pk)
        watch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
