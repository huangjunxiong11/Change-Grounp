from moviepy.editor import VideoFileClip


# file_name = r'../mp4/2020-04-22/WBFA720-LHD202004/1.mp4'
#
# clip = VideoFileClip(file_name)
# size = clip.size
# # (clip.crop(x1=20, y1=20, x2=200, y2=200).write_videofile('裁剪指定区域.mp4'))
#
# # (clip.crop(x_center=size[0]/2, y_center=size[1]/2, width=360, height=640).write_videofile('以中心点为准进行视频尺寸的裁剪.mp4'))
#
# clip2 = VideoFileClip('裁剪指定区域.mp4').resize(size)
# clip2.write_videofile("小尺寸butong比例缩放到大尺寸.mp4")
#
# pass
def changesize(file_name):
    ship = VideoFileClip(file_name)
    w, h = ship.size
    w_r = w / 720
    h_r = h / 1280
    # if w_r >= 1 and h_r >= 1:
    #     minr = min(w_r, h_r)
    #     clip = VideoFileClip(file_name).resize([w / minr, h / minr])
    # elif w_r >= 1 and h_r <= 1:
    #     clip = VideoFileClip(file_name).resize([w / h_r, h / h_r])
    # elif w_r <= 1 and h_r >= 1:
    #     clip = VideoFileClip(file_name).resize([w / w_r, h / w_r])
    # elif w_r <= 1 and h_r <= 1:
    #     minr = min(w_r, h_r)
    #     clip = VideoFileClip(file_name).resize([w / minr, h / minr])
    minr = min(w_r, h_r)
    clip = ship.resize([w / minr, h / minr])
    jianqie = clip.crop(x_center=w / 2, y_center=h / 2, width=720, height=1280)
    end = ship.duration  # seconds
    if end > 20:
        shijian = jianqie.subclip(t_start=end/2, t_end=end/2+10)
    elif 10 <= end <= 20:
        shijian = jianqie.subclip(t_start=0, t_end=10)
    elif end < 10:
        shijian = jianqie.subclip(t_start=0, t_end=end)
    shijian.write_videofile('output有音频视频.mp4')
    # (clip.crop(x_center=w / 2, y_center=h / 2, width=720, height=1280).write_videofile(
    #     '飞机任意视频尺寸的保存.mp4'))
    # pass


if __name__ == '__main__':
    file_name = r'../output/2020-04-23/WBFA720/WBFA720-LHD202005-1.mp4'
    changesize(file_name)
