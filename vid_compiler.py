import requests
import datetime
import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tqdm import tqdm

def check_archives():
    headers = {'authorization':'YOUR_TOKEN_HERE'}
    d_messages = requests.get('https://discordapp.com/api/v6/channels/YOUR_CHANNEL_HERE/messages?limit=100', headers=headers)  
    messages = d_messages.json()
    links = []
    for message in messages:
        if 'streamable' in message['content'] and (datetime.datetime.today() - datetime.datetime.strptime(message['timestamp'].split('T')[0],'%Y-%m-%d')).days < 7:
            links.append(message['content'])

    return links


def download_content():
    videos = check_archives()

    ids = [x.split('/')[-1].strip() for x in videos]
    random.shuffle(ids)

    for i in tqdm(ids):
        r = requests.get(f'https://api.streamable.com/videos/{i}')
        j = r.json()
        url = f"https:{j['files']['mp4']['url']}"
        with open(f'storage/{i}.mp4', 'wb') as file:
            r2 = requests.get(url)
            file.write(r2.content)

def stitch_video():
    files = os.listdir('storage')
    clips = []
    for file in files:
        clips.append(VideoFileClip(f'storage/{file}', target_resolution=(1080,1920)))
    random.shuffle(clips)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(f'out-{datetime.datetime.now()}.mp4', fps=60, preset='superfast', threads=4)


if __name__ == "__main__":
    download_content()
    stitch_video() 

