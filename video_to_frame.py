from pytube import YouTube
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--video_ext', default='eKMp-4Mmqdw',
                    help='extension in YT url after v=')
parser.add_argument('--res', default='240p',
                    help='desired download resolution')
parser.add_argument('--video_name', default='usc_village',
                    help='name of video')
args = parser.parse_args()

YT_ROOT = 'https://www.youtube.com/watch?v='
VIDEO_URL = args.video_ext
RES = args.res
VIDEO_NAME = args.video_name


# Function that returns array of frames given YouTube video url, res, name
def video_to_frames(video_url, res, video_name, length=20):
    """
    video_url: url of youtube video
    res: resolution; eg '144p'
    video_name: name of video
    """
    # grab YouTube object from url and download it to data/
    yt = get_yt(video_url)
    if yt is None:
        return
    download_video(yt, res, video_name)

    # trim everything but first 'length' seconds of video
    ffmpeg_extract_subclip('data/' + video_name + '.mp4', 0, 20,
                           targetname='trimmed_' + video_name + '.mp4')


# Helper function to download YT vid given YouTube Object
def download_video(yt, res, name='vid'):
    """
    yt: youtube object
    res: resolution; eg '144p'
    name: name of video
    """
    try:
        # filter by resolution and to mp4
        stream = yt.streams.filter(res=RES, mime_type='video/mp4').all()[0]
        stream.download(output_path='data/', filename=name)

    except:
        print("Connection Error Download Vid", res)
        return False

    return True


# Helper function to return YouTube object given link
def get_yt(link):
    print(link)
    try:
        # object creation using YouTube which was imported in the beginning
        yt = YouTube(link, )
    except:
        print("YT Error")
        return None

    return yt


video_to_frames(YT_ROOT+VIDEO_URL, RES, VIDEO_NAME)