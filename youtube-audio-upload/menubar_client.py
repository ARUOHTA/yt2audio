import rumps
from audio_download import audio_download

# MacのMenubarに常駐させる、10秒おきに自動実行する
class RumpsTest(rumps.App):
    @rumps.timer(10)
    def repetition(self, _):
        try:
            audio_download()
        except:
            pass
            
    @rumps.clicked("Download")
    def download(self, _):
        audio_download()

def main():
    RumpsTest("YT", icon="icon.png").run()