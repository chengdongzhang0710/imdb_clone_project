from django.contrib import admin
from watchlist_app.models import StreamPlatform, Watch, Review

# Register your models here.
admin.site.register(StreamPlatform)
admin.site.register(Watch)
admin.site.register(Review)
