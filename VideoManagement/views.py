from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse

import requests

from .models import VideoInfo

import json


def retrieve_view_count(videos):
    url = settings.VIEW_COUNT_URL
    char = '?'
    for video in videos:
        url += "%cid=%s" % (char, video.real_id)
        char = '&'

    response = requests.get(url)
    json_data = response.json()

    success = json_data['success']
    if success:
        for video in videos:
            video.view_count = json_data[video.real_id]

    return success

def home_page(request):
    return redirect(reverse('list_videos'))

def list_videos(request):
    video_list = VideoInfo.objects.filter(is_disabled=False).order_by('-id')

    paginator = Paginator(video_list, 12) # Allow only 12 pages for each page
    page = int(request.GET.get('page', 1))
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    finally:
        # Update view_count for each video objects
        success = retrieve_view_count(videos)

    if success:
        # Create url for images stored in cloudinary
        cloudinary_img_url = \
            "https://res.cloudinary.com/%s/image/upload/v1555853606/nogistream" % settings.CLOUDINARY_NAME

        return render(request, 'list.html', {'videos': videos, 'cloudinary_img_url': cloudinary_img_url})
    else:
        return HttpResponse(status_code=503) # Service Unavailable

def search_videos(request):
    search_type = request.GET.get('type', None)
    search_value = request.GET.get('value', None)

    search_value = search_value.replace('+', ' ')

    if search_type == "Title":
        searched_video_list = VideoInfo.objects.filter(is_disabled=False).filter(title__icontains=search_value)
    elif search_type == "Performer":
        searched_video_list = VideoInfo.objects.filter(is_disabled=False).filter(performer__icontains=search_value)

    # Update view_count for each video objects
    success = retrieve_view_count(videos)
    
    if success:
        return render(request, 'list.html', {'videos': searched_video_list})
    else:
        return HttpResponse(status_code=503)

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

    # Retrieve video view count
    response = requests.get(settings.VIEW_COUNT_URL + "?p=" + video.real_id)
    video.view_count = (response.json())[video.real_id]

    # Get random videos except the one being viewed
    other_videos = VideoInfo.objects.filter(is_disabled=False).exclude(id=video_id)

    # Retrieve other video's view count
    success = retrieve_view_count(other_videos)

    if success:
        # Create url for images stored in cloudinary
        cloudinary_img_url = \
            "https://res.cloudinary.com/%s/image/upload/v1555853606/nogistream" % settings.CLOUDINARY_NAME

        # Render template
        return render(request, 'view.html', 
            {
                'video': video,
                'other_videos': other_videos,
                'cloudinary_img_url': cloudinary_img_url
            }
        )
    else:
        return HttpResponse(status_code=503)

    

