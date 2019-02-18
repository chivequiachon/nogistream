from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import VideoInfo

import json


def list_videos(request):
    video_list = VideoInfo.objects.all().order_by('-id')
    paginator = Paginator(video_list, 12)
    page = int(request.GET.get('page', 1))
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'videos': videos})

def search_videos(request):
    search_type = request.GET.get('type', None)
    search_value = request.GET.get('value', None)

    search_value = search_value.replace('+', ' ')

    if search_type == "Title":
        searched_video_list = VideoInfo.objects.filter(title__icontains=search_value)
    elif search_type == "Performer":
        searched_video_list = VideoInfo.objects.filter(performer__icontains=search_value)

    return render(request, 'list.html', {'videos': searched_video_list})

def view_video(request):
    # Get query string
    video_id = request.GET.get('id', None)
    if video_id is None:
        return HttpResponse(status=404)
    
    # Get video object from db using id
    video = get_object_or_404(VideoInfo, id=video_id)

    # Render template
    return render(request, 'view.html', {'video': video})

def increment_video_view_count(request):
    if request.is_ajax() and request.method == 'POST':
        video_id_json = json.loads(request.body)
        video_id = video_id_json['id']

        # Get video object from db using id and increment
        video = get_object_or_404(VideoInfo, id=video_id)
        video.increment_view_count()

        return HttpResponse(status=200)
    return HttpResponse(status=404)

    

