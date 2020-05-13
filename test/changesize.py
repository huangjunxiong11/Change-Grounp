from moviepy.editor import VideoFileClip
import os
import argparse
import sys
import time
import logging

parser = argparse.ArgumentParser(description='Classify some images.')
# parser.add_argument('--video', help='father path of video', default="/mnt/nfs/backgroup/", type=str, dest="fpov")
# parser.add_argument('--pictrue', help='father path of pictrue', default="/mnt/nfs/backgroup/", type=str, dest="fpop")
# parser.add_argument('--output', help='father path of output', default="/mnt/nfs/backgroup/", type=str, dest="fpoo")
parser.add_argument('--video', help='father path of video', default="../", type=str, dest="fpov")
parser.add_argument('--pictrue', help='father path of pictrue', default="../", type=str, dest="fpop")
parser.add_argument('--output', help='father path of output', default="../", type=str, dest="fpoo")
args = parser.parse_args(sys.argv[1:])

# 存放视频的上级目录
fpov = args.fpov
# 存放图片的上级目录
fpop = args.fpop
# 存放输出的上级目录
fpoo = args.fpoo


def get_today_sc_videohome(Today):
    while True:
        sc = fpov + 'sc/' + Today
        root = fpov + 'VideoHome/' + Today
        if os.path.exists(sc):
            Situations = os.listdir(sc)
            Mp4s = []

            for key in Situations:
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                # mp4s += glob.glob(os.path.join(root, key, '*.mp4'))
                files = os.listdir(os.path.join(sc, key))
                for i, var in enumerate(files):
                    a = os.path.join(sc, key, var)
                    b = os.path.join(root, key, var)
                    Mp4s.append([a, b])
            return Mp4s

        else:
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if today == Today:
                logging.warning('not found folder {}, sleep five minutes'.format(sc))
                time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉一小时之后再进行检测
            else:
                Today = today


def changesize(inputname, outputname):
    ship = VideoFileClip(inputname)
    w, h = ship.size
    w_r = w / 720
    h_r = h / 1280
    minr = min(w_r, h_r)
    new_w = int(w / minr)
    new_h = int(h / minr)
    clip = ship.resize([new_w, new_h])
    jianqie = clip.crop(x_center=int(new_w / 2), y_center=int(new_h / 2), width=720, height=1280)
    end = ship.duration
    if end > 20:
        shijian = jianqie.subclip(t_start=end / 2, t_end=end / 2 + 10)
    elif 10 <= end <= 20:
        shijian = jianqie.subclip(t_start=0, t_end=10)
    else:
        shijian = jianqie.subclip(t_start=0, t_end=end)
    patha, filename = os.path.split(outputname)
    if not os.path.exists(patha):
        os.makedirs(patha)
    shijian.write_videofile(outputname)


if __name__ == '__main__':
    Today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    names = get_today_sc_videohome(Today=Today)
    for i, name in enumerate(names):
        changesize(name[0], name[1])
    pass