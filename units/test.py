from moviepy.editor import *


def comvideo(inputvideo, endvideo):
    """
    视频合成
    :param inputvideo:合成的第一段视频
    :param endvideo:合成的第二段视频
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '视频空间合成{}.mp4'.format(endvideo)
    outname = path + a
    video1 = VideoFileClip(inputvideo)
    video2 = VideoFileClip(endvideo)
    video3 = CompositeVideoClip([video1, video2])
    video3.write_videofile(outname)
