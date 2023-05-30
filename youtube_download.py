import sys, os, re
import glob
import shutil
from tqdm import tqdm
#from ytmusicapi import YTMusic
import yt_dlp


def audio_download():
    # YouTubeから動画の音声をダウンロード 

    # 専用のプレイリスト
    URL = ["https://www.youtube.com/playlist?list=PLfmdYkcYq5IS41-Xt2EsJ46nCmfheA6tG"]
    download_dir = "/Users/aruohta/dev/youtube-audio-upload/downloaded"
    upload_dir = "/Users/aruohta/Music/Music/Media.localized/Automatically Add to Music.localized/"
    ext = 'm4a'

    ydl_opts = {
        'download_archive': '/Users/aruohta/dev/youtube-audio-upload/archive.txt', 
        'outtmpl': f'{download_dir}/%(title)s'+'.'+ext,
        'format': f"{ext}/bestaudio/best", 
        'writethumbnail': 'true', 
        'merge_output_format': ext,
        'postprocessors': [
            { # Embed metadata in video using ffmpeg. 
                'key': 'FFmpegMetadata', 
                'add_metadata': True, 
            },{
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False, 
            },{
                'key': 'MoveFilesAfterDownload',
            }
        ],
    }

    # プレイリスト上の動画を全てダウンロード
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)
        print(error_code)
        
        
    # Apple Musicに音声をアップロード 
    files = glob.glob(os.path.join(download_dir, f"*.{ext}"), recursive=True)
    for f in files:
        shutil.move(f, upload_dir)


if __name__ == "__main__":
    audio_download()


'''
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
'''
