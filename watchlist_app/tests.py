from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Password@123')
        self.client.force_authenticate(user=self.user)
        self.stream = models.StreamPlatform.objects.create(name='example',
                                                           about='description',
                                                           website='https://example.com')

    def test_streamplatform_create(self):
        data = {
            'name': 'testcase',
            'about': 'description',
            'website': 'https://testcase.com',
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Password@123')
        self.client.force_authenticate(user=self.user)
        self.stream = models.StreamPlatform.objects.create(name='example',
                                                           about='description',
                                                           website='https://example.com')
        self.watch = models.Watch.objects.create(title='example',
                                                 storyline='description',
                                                 platform=self.stream,
                                                 active=True)

    def test_watch_create(self):
        data = {
            'title': 'testcase',
            'storyline': 'description',
            'platform': self.stream,
            'active': True,
        }
        response = self.client.post(reverse('watch-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watch_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watch_detail(self):
        response = self.client.get(reverse('watch-detail', args=(self.watch.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Password@123')
        self.client.force_authenticate(user=self.user)
        self.stream = models.StreamPlatform.objects.create(name='example',
                                                           about='description',
                                                           website='https://example.com')
        self.watch = models.Watch.objects.create(title='example',
                                                 storyline='description',
                                                 platform=self.stream,
                                                 active=True)
        self.watch2 = models.Watch.objects.create(title='example2',
                                                  storyline='description2',
                                                  platform=self.stream,
                                                  active=True)
        self.review = models.Review.objects.create(reviewer=self.user,
                                                   rating=5,
                                                   description='comment',
                                                   watch=self.watch2,
                                                   active=True)

    def test_review_create(self):
        data = {
            'reviewer': self.user,
            'rating': 5,
            'description': 'comment',
            'watch': self.watch,
            'active': True,
        }
        response = self.client.post(reverse('review-create', args=(self.watch.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_update(self):
        data = {
            'reviewer': self.user,
            'rating': 5,
            'description': 'updated comment',
            'watch': self.watch,
            'active': True,
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watch.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_review(self):
        response = self.client.get('/watch/review/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
