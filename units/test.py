# ffmpeg -i 1.mp4 -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 147fss.mp4
# -i 输入的视频文件
# -r 每一秒的帧数,一秒10帧大概就是人眼的速度
# -pix_fmt 设置视频颜色空间 yuv420p网络传输用的颜色空间 ffmpeg -pix_fmts可以查看有哪些颜色空间选择
# -vcodec  软件编码器，通用稳定
# -preset 编码机预设  编码机预设越高占用CPU越大 有十个参数可选 ultrafast superfast veryfast(录制视频选用) faster fast medium(默认) slow slower veryslow(压制视频时一般选用) pacebo
# -profile:v 压缩比的配置 越往左边压缩的越厉害，体积越小 baseline(实时通信领域一般选用，画面损失越大) Extended Main(流媒体选用) High(超清视频) High 10 High 4:2:2 High 4:4:4(Predictive)
# -level:v 对编码机的规范和限制针对不通的使用场景来操作,也就是不同分辨率设置不同的值
# -crf 码率控制模式 用于对画面有要求，对文件大小无关紧要的场景  0-51都可以选择 0为无损 一般设置18 - 28之间 大于28画面损失严重
# -acodec 设置音频编码器


import sys

from PIL import Image
import os
import zlib
import threading
import platform


class ZipPictureOrVideo(object):
    """
    压缩图片、视频
    """

    def __init__(self, filePath, inputName, outName=""):
        self.filePath = filePath  # 文件地址
        self.inputName = inputName  # 输入的文件名字
        self.outName = outName  # 输出的文件名字
        self.system_ = platform.platform().split("-", 1)[0]
        if self.system_ == "Windows":
            self.filePath = (self.filePath + "\\") if self.filePath.rsplit("\\", 1)[-1] else self.filePath
        elif self.system_ == "Linux":
            self.filePath = (self.filePath + "/") if self.filePath.rsplit("/", 1)[-1] else self.filePath
        self.fileInputPath = self.filePath + inputName
        self.fileOutPath = self.filePath + outName

    @property
    def is_picture(self):
        """
        判断文件是否为图片
        :return:
        """
        picSuffixSet = {"BMP", "GIF", "JPEG", "TIFF", "PNG", "SVG", "PCX", "WMF", "EMF", "LIC", "EPS", "TGA", "JPG"}
        suffix = self.fileInputPath.rsplit(".", 1)[-1].upper()
        if suffix in picSuffixSet:
            return True
        else:
            return False

    @property
    def is_video(self):
        """
        判断文件是否为视频
        :return:
        """
        videoSuffixSet = {"WMV", "ASF", "ASX", "RM", "RMVB", "MP4", "3GP", "MOV", "M4V", "AVI", "DAT", "MKV", "FIV",
                          "VOB"}
        suffix = self.fileInputPath.rsplit(".", 1)[-1].upper()
        if suffix in videoSuffixSet:
            return True
        else:
            return False

    def compress_picture(self):
        """
        压缩图片
        :return:
        """
        fpsize = os.path.getsize(self.fileInputPath) / 1024  # 获得图片多少K   os.path.getsize(self.picPath)返回的是字节
        if fpsize >= 50.0:  # 是否大于50K
            im = Image.open(self.fileInputPath)  # 打开图片
            imBytes = im.tobytes()  # 把图片转换成bytes流
            imBytes = zlib.compress(imBytes, 5)  # 对图像字节串进行压缩
            im2 = Image.frombytes('RGB', im.size, zlib.decompress(imBytes))  # 压缩成新的图片
            if self.outName:
                im2.save(self.fileOutPath)  # 不覆盖原图
                return (self.fileOutPath, os.path.getsize(self.fileOutPath))
            else:
                im2.save(self.fileInputPath)  # 覆盖原图
                return (self.fileInputPath, os.path.getsize(self.fileInputPath))
        else:
            return True

    def compress_video(self):
        """
        压缩视频

        :return:
        """
        fpsize = os.path.getsize(self.fileInputPath) / 1024
        if fpsize >= 150.0:  # 大于150KB的视频需要压缩
            if self.outName:
                compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(
                    self.fileInputPath, self.fileOutPath)
                isRun = os.system(compress)
            else:
                compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(
                    self.fileInputPath, self.fileInputPath)
                isRun = os.system(compress)
            if isRun != 0:
                return (isRun, "没有安装ffmpeg,在Linux使用【apt install ffmpeg】安装，windows去【ffmpeg】官网下载")
            return True
        else:
            return True

    def start_compress_pic(self, is_async=True):
        """
        开始压缩图片
        :param is_async: 是否为异步压缩，默认为TRue
        :return:
        """
        if is_async:
            # 异步保存打开下面的代码，注释同步保存的代码
            thr = threading.Thread(target=self.compress_picture)
            thr.start()
        else:
            # 下面为同步保存
            self.compress_picture()

    def start_compress_video(self, is_async=True):
        """
        开始压缩视频
        :param is_async: 是否为异步压缩，默认为TRue
        :return:
        """
        if is_async:
            # 异步保存打开下面的代码，注释同步保存的代码
            thr = threading.Thread(target=self.compress_video)
            thr.start()
        else:
            # 下面为同步代码
            self.compress_video()


if __name__ == "__main__":
    # 输入文件路径
    args = sys.argv[1:]
    file = ZipPictureOrVideo(args[0], args[1], args[2])
    if file.is_picture:
        print(file.start_compress_pic())
    elif file.is_video:
        print(file.start_compress_video())
    else:
        print('该文件不是图片或者视频')
