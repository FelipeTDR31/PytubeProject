import json
from django.http import JsonResponse
from django.shortcuts import render
from pytubefix import YouTube
from moviepy.editor import *
import random
import ffmpeg
# Create your views here.

def merge_streams(video_path, audio_path, output_path):
    fps = 25
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(output_path, fps=fps)

def merge_video_audio(video_path, audio_path, output_path):
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    ffmpeg.output(input_video, input_audio, output_path).run(overwrite_output=True)

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
        output_path = "C:/Users/Prefeitura/Downloads/"+yt.title+".mp4"
        merge_video_audio(videoPath, audioPath, output_path)

        return JsonResponse({'status': 'success'})

