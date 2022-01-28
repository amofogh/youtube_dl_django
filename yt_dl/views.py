from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from .forms import link_form, download_video_form
from .models import Youtube_post, Video_detail
from django.conf import settings

from pytube import YouTube

# from os import mkdir
# from os.path import isdir
# from re import findall
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import WebVTTFormatter
#

# Create your views here.
from .utils import bytes_to


def home(request):
    context = {
        'get_link': None,
        'files': []
    }
    linkForm = link_form(request.GET or None)
    context['get_link'] = linkForm
    if linkForm.is_valid():
        link = linkForm.cleaned_data['link']
        post = YouTube(link)
        types = []
        try:
            videos = post.streams.filter(progressive=True, mime_type="video/mp4")
            audios = post.streams.filter(only_audio=True)
            types.append(videos)
            types.append(audios)
        except:
            return HttpResponse(status=500)
        for file_type in types:
            the_type = file_type[0].type
            files_info = []
            for file in file_type:

                if the_type == 'video':
                    quality = file.resolution
                else:
                    quality = file.abr

                downloadForm = download_video_form(request.POST or None,
                                                   initial={'link': link, 'quality': quality, 'file_type': the_type})
                # .2f mean 2 number in decimal digits
                size = format(bytes_to(file.filesize, 'm'), '.2f')
                files_info.append(
                    {'quality': quality, 'mimetype': file.mime_type, 'size': size,
                     'download_form': downloadForm})

            context['files'].append(files_info)

    # videos_info = []
    # for video in videos:
    #     quality = video.resolution
    #     downloadForm = download_video_form(request.POST or None,
    #                                        initial={'link': link, 'quality': quality})
    #     # .2f mean 2 number in decimal digits
    #     size = format(bytes_to(video.filesize, 'm'), '.2f')
    #     videos_info.append(
    #         {'quality': quality, 'mimetype': video.mime_type, 'size': size,
    #          'download_form': downloadForm})
    #
    # context['videos_info'] = videos_info
    #
    # audios_info = []
    # for audio in audios:
    #     quality = audio.abr
    #     downloadForm = download_video_form(request.POST or None,
    #                                        initial={'link': link, 'quality': quality})
    #     # .2f mean 2 number in decimal digits
    #     size = format(bytes_to(audio.filesize, 'm'), '.2f')
    #     audios_info.append(
    #         {'quality': quality, 'mimetype': audio.mime_type, 'size': size,
    #          'download_form': downloadForm})
    #
    # context['audios_info'] = audios_info

    return render(request, 'home.html', context)


def download(request):
    downloadForm = download_video_form(request.POST or None)
    if downloadForm.is_valid():
        link = downloadForm.cleaned_data['link']
        quality = downloadForm.cleaned_data['quality']
        file_type = downloadForm.cleaned_data['file_type']
        post = YouTube(link)
        title = post.title

        if file_type == 'video':
            stream_video = post.streams.filter(resolution=quality, progressive=True).first()
        elif file_type == 'audio':
            stream_video = post.streams.filter(abr=quality).first()
        else:
            raise Http404('Not Found!!')

        mime_type = stream_video.mime_type
        ext = ''
        if mime_type == 'audio/mp4':
            ext = '.mp3'
        elif mime_type == 'video/mp4':
            ext = '.mp4'
        elif mime_type == 'audio/webm':
            ext = '.webm'

        # video mean the different quality of the main video like 360p or 720p
        youtube_video = Youtube_post.objects.filter(link=link).first()
        if youtube_video is None:
            youtube_video = Youtube_post.objects.create(title=title, link=link)

        video = youtube_video.video_detail_set.filter(quality=quality).first()
        if video:
            return FileResponse(video.file)

        stream_video.download(f'{settings.MEDIA_ROOT}/files', filename=f'{title}-{quality}{ext}')
        video = youtube_video.video_detail_set.create(quality=quality, file=f'files/{title}-{quality}{ext}')
        # i dont know how return file with web servers like nginx so i just return the file
        return FileResponse(video.file)

    return HttpResponse(status=500)
