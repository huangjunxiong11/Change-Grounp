from moviepy.editor import VideoFileClip
import os


def setbitrate(inputvideo, bitrate):
    """
    改变视频码率，降低码率也可以实现对视频大小的最优化压缩
    :param inputvideo:
    :param bitrate: 例如600k
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '设置码率{}.mp4'.format(bitrate)
    name = path + a
    cmd = 'ffmpeg -i ' + inputvideo + ' -b:v ' + str(bitrate) + 'k ' + name
    # 执行cmd命令
    os.system(cmd)


setbitrate('output有音频视频.mp4', 600)
