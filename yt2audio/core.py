import sys, os, re
import json
import glob
import shutil
from tqdm import tqdm

import yt_dlp
import rumps

def audio_download():
    # YouTubeから動画の音声をダウンロード 

    params_json = open("./yt2audio/setting.json", "r")
    params = json.load(params_json)
    
    url_playlist = params["url_playlist"]   # 専用のYouTubeプレイリストのURL
    download_dir = params["download_dir"]   # ダウンロードした音声の保存先
    upload_dir   = params["upload_dir"]     # 音声のアップロード先：Apple Musicの「”ミュージック”に自動的に追加」フォルダ
    archive_file = params["archive_file"]   # アーカイブファイル。
    ext          = params["ext"]            # 音声の拡張子：m4aやmp3など

    ydl_opts = {
        'download_archive': archive_file, 
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
        error_code = ydl.download(url_playlist)
        print(error_code)
        
        
    # Apple Musicに音声をアップロード 
    files = glob.glob(os.path.join(download_dir, f"*.{ext}"), recursive=True)
    for f in files:
        shutil.move(f, upload_dir)


# MacのMenubarに常駐させる、10秒おきに自動実行する
class RumpsTest(rumps.App):
    @rumps.timer(10)
    def repetition(self, _):
        try:
            audio_download()
        except:
            pass

def main():
    RumpsTest("YT", icon="icon.png").run()
    
if __name__ == "__main__":
    audio_download()