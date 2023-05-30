# yt2audio

This is the repository for downloading youtube vides as audio files
YouTubeの動画から音声を抜き出して、音声ファイルとしてローカルにダウンロードします。

# installation
```sh
brew install poetry # poetryがない場合
git clone https://github.com/ARUOHTA/yt2audio.git
cd yt2audio
make init
```

Then, you need to edit yt2audio/setting.json. Below is example.
```json
{
    "url_playlist" : "https://www.youtube.com/playlist?list=**************************", 
    "download_dir" : "~/dev/yt2audio/yt2audio/downloaded", 
    "upload_dir"   : "~/Music/Music/Media.localized/Automatically Add to Music.localized/",
    "archive_file" : "~/dev/yt2audio/yt2audio/archive.txt", 
    "ext"          : "m4a"
}
```
**url_playlist** : url to the playlist which contains videos you want to download.  
**download_dir** : directory where audios are downloaded.  
**upload_dir**   : directory where audios are moved after download is completed.  
**archive_file** : text file which memoirze IDs of videos which are already downloaded.  
**ext**          : extension of audio files.  

# Run
`make run` or `poetry run python -m yt2audio`  

# cation⚠
This program is for me.  
I just execute this on MacOS Ventura(M2) only.  
