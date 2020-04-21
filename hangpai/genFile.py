import glob
import os
import time
import logging
Today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
fpop = '../../'
# todo 获取当日背景图片
def get_today_jpg(Today):
    root = fpop + 'videoHome/' + Today
    while True:
        if os.path.exists(root):
            Situations = os.listdir(root)
            Mp4s = {}
            mp4s = []
            for key in Situations:
                if key == '.DS_Store' or key == '._.DS_Store':
                    continue
                mp4s += glob.glob(os.path.join(root, key, '*.mp4'))
                Mp4s[key] = mp4s
            return Mp4s
        else:
            logging.warning('not found folder {}, sleep five minutes'.format(root))
            time.sleep(60 * 5)  # 如果没有这个文件夹，睡觉一小时之后再进行检测












# images += glob.glob(os.path.join(root, name, '*.png'))
if __name__ == '__main__':

    Mp4s = get_today_jpg(Today=Today)