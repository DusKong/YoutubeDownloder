import yt_dlp
from tkinter import messagebox
import os
import configparser

TITLE = 'YoutubeDownloder'
INPUT_PATH = os.getcwd() + '/inputs'
OUTPUT_PATH = os.getcwd() + '/outputs'

url_file = configparser.ConfigParser(interpolation = None)

def format_selector(ctx):
    formats = ctx.get('formats')[::-1]

    best_video = next(f for f in formats
        if f['ext'] == 'mp4' and f['acodec'] == 'none')

    best_audio = next(f for f in formats
        if f['ext'] == 'm4a' and f['vcodec'] == 'none')

    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': 'mp4',
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

def get_url_list():
    result = []
    for fname in os.listdir(INPUT_PATH):
        if(fname[-4:] == '.url'):
            file = INPUT_PATH + '/' + fname
            url_file.read(file)
            url = url_file['InternetShortcut']['URL']
            result.append(url)

    return result

options = {
	'format': format_selector,
    'outtmpl': OUTPUT_PATH + '/%(title)s.%(ext)s',
	'merge_output_format': 'mp4',
    'ignoreerrors': 'only_download'
}

def youtube_download():
    ##if os.path.exists(INPUT_PATH + '/youtube.com_cookies.txt'):
        ##options['cookiefile'] = INPUT_PATH + '/youtube.com_cookies.txt'

    url_list = get_url_list()
    if len(url_list) == 0:
        messagebox.showinfo(TITLE, 'ダウンロードするファイルが見つかりません')
        return

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url_list)

    messagebox.showinfo(TITLE, 'ダウンロードに成功しました！')

def main():
    if not os.path.isdir(INPUT_PATH) or not os.path.isdir(OUTPUT_PATH):
        os.makedirs(INPUT_PATH, exist_ok=True)
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        return

    youtube_download()

main()