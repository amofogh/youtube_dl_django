from os import path

from django.db import models


def get_filename(filepath):
    basename = path.basename(filepath)
    name, ext = path.splitext(basename)
    return name, ext


def upload_file_path(instance, filename):
    name, ext = get_filename(filename)
    title = instance.youtube_post.title
    new_name = f'{title}{ext}'
    return f'videos/{new_name}'


# Create your models here.

class Youtube_post(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(unique=True)

    def __str__(self):
        return self.title


class Video_detail(models.Model):
    youtube_post = models.ForeignKey(Youtube_post, models.CASCADE)
    quality = models.CharField(max_length=30)
    file = models.FileField(upload_to=upload_file_path)

    def __str__(self):
        return f'{self.youtube_post.title}/{self.quality}'
