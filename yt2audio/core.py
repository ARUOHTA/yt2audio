import json
import shutil
from pathlib import Path

import yt_dlp
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
import rumps

def audio_download():
    # YouTubeから動画の音声をダウンロード 

    params_json = open("./yt2audio/setting.json", "r")
    params = json.load(params_json)
    
    url_playlist = params["url_playlist"]   # 専用のYouTubeプレイリストのURL
    download_dir = params["download_dir"]   # ダウンロードした音声の保存先
    upload_dir   = params["upload_dir"]     # 音声のアップロード先：Apple Musicの「”ミュージック”に自動的に追加」フォルダ
    archive_file = params["archive_file"]   # アーカイブファイル。
    
    ydl_opts = {
        'download_archive': archive_file, 
        'outtmpl': f'{download_dir}/%(title)s',
        'format': f"bestaudio/best", 
        'postprocessors': [
               {'key': 'FFmpegExtractAudio',
                'preferredcodec': "mp3",
                'preferredquality': '192'},
               {'key': 'FFmpegMetadata'},
           ],
    }
    
    # プレイリスト上の動画を全てダウンロード
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url_playlist)
        print(error_code)
    
    # Apple Musicに音声をアップロード 
    for f in Path(download_dir).iterdir():
        if f.suffix == ".mp3":
            # mp3をApple Losslessに変換
            sound = AudioSegment.from_file(f, format="mp3")
            tag = EasyID3(f)
            artist = tag['artist'][0]
            sound.export(f.with_suffix('.m4a'), 
                         format="ipod", 
                         codec="alac", 
                         tags={"artist": artist})
            
            if f.with_suffix(".m4a").exists():
                print(f"converted: {f.stem}")
                f.unlink(missing_ok=True)
                # AppleMusicの管理下フォルダに移動
                shutil.move(f.with_suffix(".m4a"), upload_dir)


# MacのMenubarに常駐させる、10秒おきに自動実行する
class RumpsTest(rumps.App):
    @rumps.timer(20)
    def repetition(self, _):
        try:
            audio_download()
        except:
            pass

def main():
    RumpsTest("YT", icon="icon.png").run()
    
if __name__ == "__main__":
    audio_download()