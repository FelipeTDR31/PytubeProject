import json
import subprocess
from django.http import JsonResponse
from django.shortcuts import render
from pytubefix import YouTube
import random
import shutil
import os
from django.http import FileResponse
from django.conf import settings
# Create your views here.

def merge_video_audio(video_path, audio_path, output_path):
    # Construct the FFmpeg command
    command = f'ffmpeg  -y -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}'

    # Run the FFmpeg command as a subprocess
    subprocess.run(command, shell=True)
    folder_path = os.path.dirname(video_path)
    shutil.rmtree(folder_path)

def download(request, name):
    if request.method == 'GET':
        output_path = "videos/"+name+".mp4"
        file = open(output_path, 'rb')
        return FileResponse(file, as_attachment=True, filename=name+".mp4", content_type='video/mp4')

def index(request):
    return render(request, 'index.html', {'requestURL': settings.REQUEST_URL})

def search(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        url = data['url']
        yt = YouTube(url)
        VideoStreams = yt.streams.filter(type='video')
        AudioStreams = yt.streams.filter(type='audio', mime_type='audio/mp4', abr="128kbps")
        streamsJson = []
        audioStreamsJson = []
        for stream in VideoStreams:
            if stream.mime_type == 'video/mp4':
                streamsJson.append({
                    'resolution': stream.resolution,
                    'itag': stream.itag
                })
        for stream in AudioStreams:
            audioStreamsJson.append({
                'itag': stream.itag
            })
        title = yt.title
        return JsonResponse({'title': title, 'streams': streamsJson, 'audioStreams': audioStreamsJson})

def prepare (request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        url = data['url']
        selectedStream = data['selectedStream']
        selectedAudioStream = data['audioStream']
        yt = YouTube(url)
        videoStream = yt.streams.get_by_itag(selectedStream)
        audioStream = yt.streams.get_by_itag(selectedAudioStream)
        randomID = random.randint(1,1000)
        videoStream.download(output_path=str(randomID), filename="video"+".mp4")
        audioStream.download(output_path=str(randomID), filename="audio"+".mp4")
        videoPath = str(randomID)+"/"+"video"+".mp4"
        audioPath = str(randomID)+"/"+"audio"+".mp4"
        output_path = "videos/"+''.join(e for e in yt.title if e.isalnum() or e == '_')+".mp4"
        file_name = ''.join(e for e in yt.title if e.isalnum() or e == '_')
        merge_video_audio(videoPath, audioPath, output_path)
        return JsonResponse({'file_name': file_name})