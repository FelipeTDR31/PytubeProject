import json
import subprocess
from django.http import JsonResponse
from django.shortcuts import render
from pytubefix import YouTube
import random
import shutil
import os
# Create your views here.

def merge_video_audio(video_path, audio_path, output_path):
    # Construct the FFmpeg command
    command = f'ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}'

    # Run the FFmpeg command as a subprocess
    subprocess.run(command, shell=True)
    folder_path = os.path.dirname(video_path)
    shutil.rmtree(folder_path)

def index(request):
    return render(request, 'index.html')

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

def download (request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        url = data['url']
        selectedStream = data['selectedStream']
        selectedAudioStream = data['audioStream']
        yt = YouTube(url)
        videoStream = yt.streams.get_by_itag(selectedStream)
        audioStream = yt.streams.get_by_itag(selectedAudioStream)
        randomID = random.randint(1,1000)
        videoStream.download(output_path="C:/Users/Prefeitura/Downloads/"+str(randomID), filename="video"+".mp4")
        audioStream.download(output_path="C:/Users/Prefeitura/Downloads/"+str(randomID), filename="audio"+".mp4")
        videoPath = "C:/Users/Prefeitura/Downloads/"+str(randomID)+"/"+"video"+".mp4"
        audioPath = "C:/Users/Prefeitura/Downloads/"+str(randomID)+"/"+"audio"+".mp4"
        output_path = "C:/Users/Prefeitura/Downloads/"+''.join(e for e in yt.title if e.isalnum() or e == '_')+".mp4"
        merge_video_audio(videoPath, audioPath, output_path)

        return JsonResponse({'status': 'success'})
