from django.contrib import admin

# Register your models here.
from yt_dl.models import Video_detail, Youtube_post

admin.site.register(Youtube_post)
admin.site.register(Video_detail)
