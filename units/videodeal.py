import os
from moviepy.editor import *


# todo 视频格式转换
def formatchange(path_in, path_out):
    """
    将mov、avi等视频格式转换为📛mp4格式
    :param path_in: 输入路径
    :param path_out: 输出路径
    :return: 无返回值
    """

    cmd = 'ffmpeg -i ' + path_in + ' -strict -2 -vcodec h264 ' + path_out
    # 执行cmd命令
    os.system(cmd)


# todo 帧率设置
def setfps(inputvideo, fps):
    """
    设置视频帧数
    :param inputvideo:
    :param fps: 帧数，例如25
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '帧数设置{}.mp4'.format(fps)
    name = path + a
    cmd = 'ffmpeg -i ' + inputvideo + ' -r ' + str(fps) + ' ' + name
    # 执行cmd命令
    os.system(cmd)


# todo 比特率设置
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


# todo 剪掉片头
def cutbegin(inputvideo, time):
    """
    剪切视频片头
    :param inputvideo: 输入视频目录
    :param time: 片头时长
    :return: 无返回值
    """
    clip1 = VideoFileClip(inputvideo)  # 读取视频对象
    path, _ = os.path.splitext(inputvideo)
    mp3 = path + '.mp3'  # 构造📛mp3保存路径
    outmp3 = path + 'out.mp3'
    end = clip1.duration  # 视频时间总长
    shenyin = clip1.audio
    outname = path + '-剪切片头.mp4'
    if shenyin != None:
        # 如果源视频有声音
        shenyin.write_audiofile(mp3)  # 提取保存视频音频

        os.system(
            "ffmpeg -i {in_path} -vn -acodec copy -ss {Start_time} -t {Dur_time}  {out_path}".format(in_path=mp3,
                                                                                                     out_path=outmp3,
                                                                                                     Start_time=time,
                                                                                                     Dur_time=end))
        if time <= end:
            clip1 = clip1.cutout(0, time)  # 切除片头
            clip1 = clip1.without_audio()  # 去除音频
            name = path + 'cut.mp4'  # 构造名字
            clip1.write_videofile(name, audio=False)  # 保存没有音频的视频
            clip1.close()

            cmd = 'ffmpeg -i ' + name + ' -i ' + outmp3 + ' -strict -2 -f mp4 ' + outname
            # 执行cmd命令
            os.system(cmd)

            # 删除中间生成的多余文件
            os.remove(mp3)
            os.remove(outmp3)
            os.remove(name)
    else:
        # 如果原视频没有声音
        if time <= end:
            clip1 = clip1.cutout(0, time)  # 切除片头
            clip1.write_videofile(outname, audio=False)  # 保存没有音频的视频
            clip1.close()


# todo 剪掉片尾
def cutend(inputvideo, time):
    """
    剪切视频片尾
    :param inputvideo: 输入视频目录
    :param time: 片尾时间节点
    :return: 无返回值
    """
    clip1 = VideoFileClip(inputvideo)  # 读取视频对象
    path, _ = os.path.splitext(inputvideo)
    mp3 = path + '.mp3'  # 构造📛mp3保存路径
    outmp3 = path + 'out.mp3'
    end = clip1.duration  # 视频时间总长
    shenyin = clip1.audio
    outname = path + '-剪切片尾.mp4'
    if shenyin != None:
        # 如果源视频有声音
        shenyin.write_audiofile(mp3)  # 提取保存视频音频

        os.system(
            "ffmpeg -i {in_path} -vn -acodec copy -ss {Start_time} -t {Dur_time}  {out_path}".format(in_path=mp3,
                                                                                                     out_path=outmp3,
                                                                                                     Start_time=0,
                                                                                                     Dur_time=time))
        if time <= end:
            clip1 = clip1.cutout(time, end)  # 切除片尾
            clip1 = clip1.without_audio()  # 去除音频
            name = path + 'cut.mp4'  # 构造名字
            clip1.write_videofile(name, audio=False)  # 保存没有音频的视频
            clip1.close()

            cmd = 'ffmpeg -i ' + name + ' -i ' + outmp3 + ' -strict -2 -f mp4 ' + outname
            # 执行cmd命令
            os.system(cmd)

            # 删除中间生成的多余文件
            os.remove(mp3)
            os.remove(outmp3)
            os.remove(name)
    else:
        # 如果原视频没有声音
        if time <= end:
            clip1 = clip1.cutout(0, time)  # 切除片头
            clip1.write_videofile(outname, audio=False)  # 保存没有音频的视频
            clip1.close()


# todo 视频裁剪
def star_subclip_end(inputvideo, startime, endtime):
    """
    剪切自己感兴趣的部分视频片段
    :param inputvideo: 输入视频目录
    :param startime: 剪辑开始时间节点
    :param endtime: 剪辑结束时间节点
    :return: 无返回值
    """
    clip1 = VideoFileClip(inputvideo)  # 读取视频对象
    path, _ = os.path.splitext(inputvideo)
    mp3 = path + '.mp3'  # 构造📛mp3保存路径
    outmp3 = path + 'out.mp3'
    end = clip1.duration  # 视频时间总长
    shenyin = clip1.audio
    outname = path + '-视频剪辑.mp4'
    if shenyin != None:
        # 如果源视频有声音
        shenyin.write_audiofile(mp3)  # 提取保存视频音频

        os.system(
            "ffmpeg -i {in_path} -vn -acodec copy -ss {Start_time} -t {Dur_time}  {out_path}".format(in_path=mp3,
                                                                                                     out_path=outmp3,
                                                                                                     Start_time=startime,
                                                                                                     Dur_time=endtime))
        if endtime <= end:
            clip1 = clip1.subclip(startime, endtime)  # 视频剪辑
            clip1 = clip1.without_audio()  # 去除音频
            name = path + 'cut.mp4'  # 构造名字
            clip1.write_videofile(name, audio=False)  # 保存没有音频的视频
            clip1.close()

            cmd = 'ffmpeg -i ' + name + ' -i ' + outmp3 + ' -strict -2 -f mp4 ' + outname
            # 执行cmd命令
            os.system(cmd)

            # 删除中间生成的多余文件
            os.remove(mp3)
            os.remove(outmp3)
            os.remove(name)
    else:
        # 如果原视频没有声音
        if endtime <= end:
            clip1 = clip1.subclip(startime, endtime)  # 视频剪辑
            clip1.write_videofile(outname, audio=False)  # 保存没有音频的视频
            clip1.close()


# todo 视频旋转
def rotation(inputvideo, rota):
    """
    将视频旋转rota度
    :param inputvideo:
    :param rota:
    :return:
    """
    video1 = VideoFileClip(inputvideo)
    video1 = video1.rotate(rota)
    path, _ = os.path.splitext(inputvideo)
    a = '视频旋转{}度.mp4'.format(rota)
    name = path + a
    video1.write_videofile(name)


# todo 视频镜像
def mirror(inputvideo, model):
    """
    视频镜像
    :param inputvideo:
    :param model: model为1表示水平镜像，为2表示垂直镜像
    :return:
    """
    video1 = VideoFileClip(inputvideo)
    path, _ = os.path.splitext(inputvideo)
    if model == 1:  # 表示水平镜像
        name = path + '水平镜像.mp4'
        (video1.fx(vfx.mirror_x).write_videofile(name, codec='libx264'))
    elif model == 2:  # 表示垂直镜像
        name = path + '垂直镜像.mp4'
        (video1.fx(vfx.mirror_y).write_videofile(name, codec='libx264'))


# todo 视频缩放
def setsize(inputvideo, w_size, h_size):
    """
    视频按尺寸进行缩放，等比例缩小相当于下调分辨率
    :param inputvideo:
    :param w_size: 视频宽度
    :param h_size: 视频高度
    :return:
    """
    ship = VideoFileClip(inputvideo)
    clip = ship.resize([w_size, h_size])
    path, _ = os.path.splitext(inputvideo)
    a = '视频缩放为{}x{}.mp4'.format(w_size, h_size)
    name = path + a
    clip.write_videofile(name)


# todo 调整视频分辨率
def setresolution(inputvideo, w_size, h_size):
    """
    调整视频分辨率
    :param inputvideo:
    :param w_size: 目标视频宽度
    :param h_size: 目标视频高度
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '调整分辨率{}x{}.mp4'.format(w_size, h_size)
    name = path + a
    cmd = 'ffmpeg -i ' + inputvideo + ' -s ' + str(w_size) + 'x' + str(h_size) + ' ' + name
    # 执行cmd命令
    os.system(cmd)


# todo 视频压缩
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


# todo 添加文字水印

# todo 添加跑马灯文字水印

# todo 画中画

# todo 添加背景音乐
def addmp3(inputvideo, mp3path):
    """
    给视频增加音频
    :param inputvideo: 输入视频目录
    :param mp3path: 输入音频目录
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '增加音频{}.mp4'.format(mp3path)
    outname = path + a
    cmd = 'ffmpeg -i ' + inputvideo + ' -i ' + mp3path + ' -strict -2 -f mp4 ' + outname
    os.system(cmd)


# todo 倍速播放
def speedplay(inputvideo, speed):
    """
    倍速播放
    :param inputvideo:
    :param speed: 速度，例如1.5
    :return:
    """

    path, _ = os.path.splitext(inputvideo)
    a = '改变速度{}.mp4'.format(speed)
    outname = path + a
    video = VideoFileClip(inputvideo)
    result = video.fl_time(lambda t: speed * t,
                           apply_to=['mask', 'video', 'audio']).set_end(video.end / speed)
    result.write_videofile(outname)


# todo 添加片头
def addstarvideo(inputvideo, starvideo):
    """
    添加片头
    :param inputvideo:
    :param starvideo:
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '增加片头{}.mp4'.format(starvideo)
    outname = path + a
    video1 = VideoFileClip(starvideo)
    video2 = VideoFileClip(inputvideo)
    video3 = concatenate_videoclips([video1, video2])
    video3.write_videofile(outname)


# todo 添加片尾
def addendvideo(inputvideo, endvideo):
    """
    添加片尾
    :param inputvideo:
    :param endvideo:
    :return:
    """
    path, _ = os.path.splitext(inputvideo)
    a = '增加片尾{}.mp4'.format(endvideo)
    outname = path + a
    video1 = VideoFileClip(inputvideo)
    video2 = VideoFileClip(endvideo)
    video3 = concatenate_videoclips([video1, video2])
    video3.write_videofile(outname)


# todo 视频分段，具体根视频的裁剪一个道理，加上一个业务逻辑就变成视频分段了

# todo 视频合成
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

# todo 自动生成电影混剪
