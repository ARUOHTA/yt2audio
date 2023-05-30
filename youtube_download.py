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
