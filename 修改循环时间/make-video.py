# -*-coding:utf-8-*-

import time
import os
import cv2
from moviepy.editor import VideoFileClip, CompositeVideoClip
# from tqdm import tqdm
from os.path import join, getsize
import argparse
import sys
import logging
parser = argparse.ArgumentParser(description='Classify some images.')
parser.add_argument('--video', help='father path of video', default="/mnt/nfs/backgroup/special/", type=str, dest="fpov")
parser.add_argument('--pictrue', help='father path of pictrue', default="/mnt/nfs/backgroup/special/", type=str, dest="fpop")
parser.add_argument('--output', help='father path of output', default="/mnt/nfs/backgroup/special/", type=str, dest="fpoo")
# parser.add_argument('--video', help='father path of video', default="../", type=str, dest="fpov")
# parser.add_argument('--pictrue', help='father path of pictrue', default="../", type=str, dest="fpop")
# parser.add_argument('--output', help='father path of output', default="../", type=str, dest="fpoo")
args = parser.parse_args(sys.argv[1:])

# 存放视频的上级目录
fpov = args.fpov
# 存放图片的上级目录
fpop = args.fpop
# 存放输出的上级目录
fpoo = args.fpoo


# todo 获取当日mov视频
def get_today_mov(Today):
    while True:
        mov_path = fpov + 'video/' + Today
        if os.path.exists(mov_path):
            Situations = os.listdir(mov_path)
            today_mov = {}
            for key in Situations:
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                varible = os.listdir(mov_path + '/' + key)
                today_mov[key] = varible
            return today_mov
        else:
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if today == Today:
                logging.warning('not found folder {}, sleep five minutes'.format(mov_path))
                time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉5小时之后再进行检测
            else:
                Today = today


# todo 获取当日背景图片
def get_today_jpg(Today):
    while True:
        jpg_path = fpop + 'pictrue/' + Today
        if os.path.exists(jpg_path):
            Situations = os.listdir(jpg_path)
            today_jpg = {}
            for key in Situations:
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                varible = os.listdir(jpg_path + '/' + key)
                today_jpg[key] = varible
            return today_jpg
        else:
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if today == Today:
                logging.warning('not found folder {}, sleep five minutes'.format(jpg_path))
                time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉一小时之后再进行检测
            else:
                Today = today


# todo 获取当日输出视频
def get_today_ouput(Today):
    out_path = fpoo + 'output/' + Today
    try:
        os.makedirs(out_path)
    except OSError:
        pass
    Situations = os.listdir(out_path)
    today_output = []
    for i in range(len(Situations)):
        key = Situations[i]
        if key == '.DS_Store' or key == '._.DS_Store':
            continue
        varible = os.listdir(out_path + '/' + key)
        for var in varible:
            var = out_path + '/' + key + '/' + var
            today_output.append(var)
    return today_output


# todo 背景图片和mov视频交叉一一配对
def img_for_mov(Today, today_jpg, today_mov):
    combination = []
    for img_key, img_value in today_jpg.items():
        for mov_key, mov_value in today_mov.items():
            if img_key == mov_key:
                for img in img_value:
                    if img.find('.') == 0 or img.find('\'') == 0:
                        continue
                    for mov in mov_value:
                        if mov.find('.') == 0 or mov.find('\'') == 0:
                            continue
                        path_img = fpop + 'pictrue/' + Today + '/' + img_key + '/' + img
                        path_mov = fpov + 'video/' + Today + '/' + mov_key + '/' + mov
                        combination.append([path_img, path_mov])
    return combination


# todo 将图片转换成视频
def jpg_become_avi(jpg, mov):
    cap = cv2.VideoCapture(mov)
    frame_number = cap.get(7)
    n = int(frame_number)
    cap = cv2.VideoCapture(mov)
    fgs = int(cap.get(cv2.CAP_PROP_FPS))
    img = cv2.imread(jpg)
    h, w, c = img.shape
    size = (w, h)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    avi = './jpg.avi'
    video_writer = cv2.VideoWriter(avi, fourcc, fgs, size)
    for i in range(n):
        video_writer.write(img)
    video_writer.release()
    return avi


# todo 将背景图片和视频mov进行合成
def mov_change_bg(avi, mov, name):
    logging.info('start processing {}'.format(name))
    clip1 = VideoFileClip(avi)
    clip3 = VideoFileClip(mov, has_mask=True)
    video = CompositeVideoClip([clip1, clip3])
    video.write_videofile(name, audio=True)
    video.close()
    logging.info('end processing {}'.format(name))

# todo 确定保存mp4目录
def create_name(Today, jpg, mov):
    a = jpg.split('/p', 1)[0]
    jpg_1 = jpg.split("/")[-1]
    jpg_2 = jpg_1.split('.', 1)[0]

    var_1 = mov.split('/')[-1]
    mov_name = var_1.split('.', 1)[0]

    name = mov_name + '-' + jpg_2

    if '（' in mov:
        var_2 = var_1.split('（', 1)[-1]
        var_3 = var_2.split('-', 1)[0]
    else:
        var_3 = var_1.split('-', 1)[0]

    path = a + '/output/' + Today + '/' + var_3 + '/'
    try:
        os.makedirs(path)
    except OSError:
        pass
    whole_path = path + name + '.mp4'
    return whole_path


# 获取文件夹大小
def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


# 日志
def console_out(logFilename):
    logging.basicConfig(
        level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename=logFilename,  # log文件名
        filemode='w')  # 写入模式“w”或“a”


# 启动程序
def run():

    while True:
        Today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        p_s_start = getdirsize(fpop + 'pictrue/' + Today)
        v_s_start = getdirsize(fpov + 'video/' + Today)
        try:
            com = img_for_mov(Today=Today,
                              today_jpg=get_today_jpg(Today),
                              today_mov=get_today_mov(Today))
        except OSError:
            logging.warning("jpg and mov is not matching")
            time.sleep(60 * 5)
            continue
        output = get_today_ouput(Today=Today)
        for i in range(len(com)):
            _ = com[i]
            name = create_name(Today=Today, jpg=_[0], mov=_[1])
            if name not in output:
                avi = jpg_become_avi(jpg=_[0], mov=_[1])
                mov_change_bg(avi=avi, mov=_[1], name=name)
                if i % 5 == 0:  # 十分钟之内检测一下有没有新增文件
                    logging.info('finding new file')
                    p_s_end = getdirsize(fpop + 'pictrue/' + Today)
                    v_s_end = getdirsize(fpov + 'video/' + Today)
                    if (p_s_end != p_s_start) and (v_s_end != v_s_start):
                        break

        com = img_for_mov(Today=Today,
                          today_jpg=get_today_jpg(Today),
                          today_mov=get_today_mov(Today))
        output = get_today_ouput(Today=Today)
        if len(com) == len(output):
            logging.warning('Had done all successfully, waiting for new file ')
            time.sleep(60 * 5)


def main():
    logPath = 'log'
    try:
        os.mkdir(logPath)
    except OSError:
        pass
    # logFilename = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '.log'
    logFilename = logPath + '/' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.log'
    console_out(logFilename=logFilename)
    run()


if __name__ == '__main__':
    main()
