import json
from django.http import JsonResponse
from django.shortcuts import render
from pytubefix import YouTube
# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        url = data['url']
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True)
        streamsJson = []
        for stream in streams:
            streamsJson.append({
                'resolution': stream.resolution,
                'itag': stream.itag
            })
        title = yt.title
        return JsonResponse({'title': title, 'streams': streamsJson})

