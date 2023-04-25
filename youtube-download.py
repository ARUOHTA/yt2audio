import sys, os, re
import glob
from tqdm import tqdm
from ytmusicapi import YTMusic
import yt_dlp

# 1. YouTubeから動画の音声をダウンロード ############################################################

# 専用のプレイリスト
URL = ['https://www.youtube.com/playlist?list=PLfmdYkcYq5IQ0tuokQYyQiyizXL069OuJ']

download_dir = './downloaded'
ydl_opts = {
    'outtmpl': f'{download_dir}/%(title)s'+'_.mp3',
    'format': 'bestaudio', 
    'max-filesize': '300M'
}

# プレイリスト上の動画を全てダウンロード
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URL)

# 2. YouTube Musicに音声をアップロード #############################################################

# detail: https://ytmusicapi.readthedocs.io/en/latest/setup.html
ytmusic = YTMusic('headers_auth.json')

# ダウンロード済みのファイルを取得
abs_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(abs_dir, './downloaded')
downloaded_files = glob.glob(os.path.join(download_dir, "*.mp3"), recursive=True)

# すでにアップロード済みのファイルを検索
uploaded_dict = ytmusic.get_library_upload_songs(limit=None) 
uploaded_files = [os.path.join(download_dir, d.get('title')) if re.search("\.mp3$", d.get('title')) else None for d in uploaded_dict]

# すでにアップロード済みのファイルはローカルから削除
for f in list(set(downloaded_files) & set(uploaded_files)):
    os.remove(f)

# まだアップロードされていないものをすべてアップロード
files = list(set(downloaded_files) - set(uploaded_files))
print("{} files found".format(len(files)))
for i, f in enumerate(files):
    print(f"{i+1}: {os.path.basename(f)}")

cnt, error_cnt = 0, 0
for f in tqdm(files):
    try:
        ytmusic.upload_song(f)
        cnt +=1
        os.remove(f) # アップロードに成功したらファイルをローカルから削除
    except:
        print("Error upload {}".format(f))
        error_cnt +=1
        pass

print("Result success {} files , fail {} files".format(cnt, error_cnt))   

