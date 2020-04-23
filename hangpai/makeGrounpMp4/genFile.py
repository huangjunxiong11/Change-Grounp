import glob
import os
import time
import logging
import random
import argparse
import sys
import logging

from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips

parser = argparse.ArgumentParser(description='Classify some images.')
# parser.add_argument('--video', help='father path of video', default="/mnt/nfs/backgroup/", type=str, dest="fpov")
# parser.add_argument('--pictrue', help='father path of pictrue', default="/mnt/nfs/backgroup/", type=str, dest="fpop")
# parser.add_argument('--output', help='father path of output', default="/mnt/nfs/backgroup/", type=str, dest="fpoo")
parser.add_argument('--video', help='father path of video', default="../../", type=str, dest="fpov")
parser.add_argument('--pictrue', help='father path of pictrue', default="../../", type=str, dest="fpop")
parser.add_argument('--output', help='father path of output', default="../../", type=str, dest="fpoo")
args = parser.parse_args(sys.argv[1:])

# 存放视频的上级目录
fpov = args.fpov
# 存放图片的上级目录
fpop = args.fpop
# 存放输出的上级目录
fpoo = args.fpoo


def get_today_mov(Today):
    root = fpov + 'video/' + Today
    while True:
        if os.path.exists(root):
            Situations = os.listdir(root)
            Movs = {}

            for key in Situations:
                movs = []
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                movs += glob.glob(os.path.join(root, key, '*.mov'))
                Movs[key] = movs
            return Movs
        # 参考：Movs = {'heng': ['../../video/2020-04-22/heng/WBFA720-LHD202004.mov', ...],
        #               'shu': ['../../video/2020-04-22/shu/WBFA720-LHD202005.mov', ...]}
        else:
            logging.warning('not found folder {}, sleep five minutes'.format(root))
            time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉一小时之后再进行检测


def get_today_mov_name(Today):
    root = fpov + 'video/' + Today
    while True:
        if os.path.exists(root):
            Situations = os.listdir(root)
            movs = []
            for key in Situations:
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                movs += glob.glob(os.path.join(root, key, '*.mov'))
            return movs
        #
        else:
            logging.warning('not found folder {}, sleep five minutes'.format(root))
            time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉一小时之后再进行检测


def get_today_videohome(Today):
    root = fpov + 'VideoHome/' + Today
    while True:
        if os.path.exists(root):
            Situations = os.listdir(root)
            Mp4s = {}

            for key in Situations:
                mp4s = []
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                mp4s += glob.glob(os.path.join(root, key, '*.mp4'))
                Mp4s[key] = mp4s
            return Mp4s
        # Mp4s = {'heng': ['../../VideoHome/2020-04-22/heng/City-29.mp4', ...],
        #          'shu': ['../../VideoHome/2020-04-22/shu/City-13.mp4', ...]}
        else:
            logging.warning('not found folder {}, sleep five minutes'.format(root))
            time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉一小时之后再进行检测


def get_tenran(var):
    """
    从var列表中随机提取十组6个元素
    :param var:
    :return:
    """
    first = random.sample(var, 10)
    tenRan = []
    for j in first:
        k = var[:]
        k.remove(j)
        child = random.sample(k, 5)
        child.insert(0, j)
        tenRan.append(child)
    return tenRan


def get_tenRan(movs, videohomes):
    # nameTenRan = {'WBFA720-LHD202004': [['../../VideoHome/2020-04-22/heng/City-19.mp4',...6个], ...],
    #               'WBA1280-HJX20200': [['../../VideoHome/2020-04-22/heng/City-15.mp4', ...6个], ...], ...}
    nameTenRan = {}
    for mov_key, mov_var in movs.items():
        for v_key, v_var in videohomes.items():
            if mov_key == v_key:
                for mov in mov_var:
                    (path, file) = os.path.split(mov)
                    name = file.split('.')[0]
                    tenRan = get_tenran(var=v_var)
                    nameTenRan[name] = tenRan
    return nameTenRan


def make_avi(m, n, path):
    name = path + '/' + str(m + 1) + '.mp4'
    if not os.path.exists(name):
        logging.info('开始生成背景视频{},包括{}'.format(name, n))
        L = []
        for i in n:
            video = VideoFileClip(i)
            L.append(video)
        final_clip = concatenate_videoclips(L)
        final_clip.to_videofile(name)
        logging.info('成功生成背景视频{},包括{}'.format(name, n))
    else:
        logging.info('已存在背景{}'.format(name))
    return name


# todo 确定保存mp4目录
def create_name(root, jpg, mov):
    (path1, file1) = os.path.split(jpg)
    jpg_2 = file1.split('.')[0]

    (path2, file2) = os.path.split(mov)
    mov_name = file2.split('.')[0]

    name = mov_name + '-' + jpg_2
    if '（' in mov:
        var_2 = mov_name.split('（', 1)[-1]
        var_3 = var_2.split('-', 1)[0]
    else:
        var_3 = mov_name.split('-', 1)[0]

    path = root + '/' + var_3 + '/'
    try:
        os.makedirs(path)
    except OSError:
        pass
    whole_path = path + name + '.mp4'
    return whole_path


# todo 将视频和视频mov进行合成
def mov_change_mp4(avi, mov, name):
    logging.info('start processing {}'.format(name))
    clip3 = VideoFileClip(mov, has_mask=True)
    end = clip3.duration  # seconds

    avivideo = VideoFileClip(avi)
    end_avi = avivideo.duration

    if end <= end_avi:
        video1 = VideoFileClip(avi).subclip(t_start=0, t_end=end)
        clip1 = video1.without_audio()
        video = CompositeVideoClip([clip1, clip3])
        video.write_videofile(name, audio=True)
        video.close()
        logging.info('start processing {}'.format(name))

    else:
        logging.error('time of mov is longer')


def make_avis(nameTenRan, Today, movs_name):
    root = fpop + 'mp4/' + Today
    outroot = fpop + 'output/' + Today
    for mov_name, tenran in nameTenRan.items():
        path = root + '/' + mov_name
        try:
            os.makedirs(path)
        except OSError:
            pass
        for movname in movs_name:
            (path, file) = os.path.split(movname)
            namemov = file.split('.')[0]
            if namemov == mov_name:
                for m, n in enumerate(tenran):
                    avi = make_avi(m=m, n=n, path=path)
                    name = create_name(root=outroot, jpg=avi, mov=movname)
                    outputnames = get_today_ouput(Today=Today)
                    if name not in outputnames:
                        mov_change_mp4(avi=avi, mov=movname, name=name)
                    else:
                        logging.info('已存在输出{}'.format(name))


# 日志
def console_out(logFilename):
    logging.basicConfig(
        level=logging.INFO,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename=logFilename,  # log文件名
        filemode='w')  # 写入模式“w”或“a”


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


def run():
    Today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    movs = get_today_mov(Today=Today)
    videohomes = get_today_videohome(Today=Today)
    movs_name = get_today_mov_name(Today=Today)
    nameTenran = get_tenRan(movs=movs, videohomes=videohomes)
    make_avis(nameTenRan=nameTenran, Today=Today, movs_name=movs_name)


# 获取文件夹大小
def getdirsize(dir):
    from os.path import join, getsize
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


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


if __name__ == '__main__':
    while True:
        main()
        logging.warning('Had done all successfully, waiting for new file , sleep five minutes')
        time.sleep(60*5)
