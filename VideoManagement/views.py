from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import VideoInfo

import json

def get_view_count(url):
    import requests
    response = requests.get(url)
    json_res = response.json()
    return int(json_res['countries'][0]['plays'])

def list_videos(request):
    video_list = VideoInfo.objects.filter(is_disabled=False).order_by('-id')

    # Update view_count for each video objects
    for video in video_list:
        video.view_count = get_view_count("https://ajax.streamable.com/%s/stats" % video.real_id)

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
        searched_video_list = VideoInfo.objects.filter(is_disabled=False).filter(title__icontains=search_value)
    elif search_type == "Performer":
        searched_video_list = VideoInfo.objects.filter(is_disabled=False).filter(performer__icontains=search_value)

    # Update view_count for each video objects
    for video in searched_video_list:
        video.view_count = get_view_count("https://ajax.streamable.com/%s/stats" % video.real_id)

    return render(request, 'list.html', {'videos': searched_video_list})

def view_video(request):
    # Get query string
    video_id = request.GET.get('id', None)
    if video_id is None:
        return HttpResponse(status=404)
    
    # Get video object from db using id
    video = get_object_or_404(VideoInfo, id=video_id)

    # Check if video is disabled
    if video.is_disabled == True:
        return HttpResponse(status=404)

    # Extract video view count
    view_count = get_view_count("https://ajax.streamable.com/%s/stats" % video.real_id)

    # Render template
    return render(request, 'view.html', {'video': video, 'view_count': view_count})

    

