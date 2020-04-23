from moviepy.editor import VideoFileClip, CompositeVideoClip
import cv2
import os
# name = 'WBFA1280-LHD200410-02_314_1422_1814_2321_2706'
mov = '../data/WBFA1280-LHD200410-02_314_1422_1814_2321_2706_3115.mov'
jpg1 = '../data/photo1.jpg'
jpg2 = '../data/photo1.jpg'
jpg = '../pictrue/2020-04-14/heng/photo1.jpg'


def jpg_become_avi(jpg, mov):
    jpg1 = jpg
    jpg2 = jpg.split('/pictrue', 1)[0] + '/pictrue2' + jpg.split('/pictrue', 1)[1]
    cap = cv2.VideoCapture(mov)
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    frame_number = int(cap.get(7))
    img1 = cv2.imread(jpg1)
    img2 = cv2.imread(jpg2)
    h, w, c = img1.shape
    size = (w, h)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    avi = './jpg3.avi'
    video_writer = cv2.VideoWriter(avi, fourcc, FPS, size)
    name = os.path.splitext(mov)[0].split('/')[-1]
    node = name.split('_')
    fps = []
    for i in range(1, len(node)):
        b = [int(j) for j in str(node[i])]
        if len(b) == 1 or len(b) == 2:
            n = node[i]
            fps.append(n)
            # print(n)
        elif len(b) == 3:
            n = b[0] * FPS + b[1] * 10 + b[2]
            fps.append(n)
            # print(n)
        elif len(b) == 4:
            n = b[0] * 10 * FPS + b[1] * FPS + b[2] * 10 + b[3]
            fps.append(n)
            # print(n)
        elif len(b) == 5:
            n = b[0] * 60 * FPS + b[1] * 10 * FPS + b[2] * FPS + b[3] * 10 + b[4]
            fps.append(n)
            # print(n)
    fps.insert(0, 0)
    fps.append(frame_number)
    # print(fps)
    duration = []
    for i in range(1, len(fps)):
        m = fps[i] - fps[i - 1]
        duration.append(m)

    # print(duration)

    for k in range(len(duration)):
        if k % 2 == 0:
            for j in range(duration[k]):
                # print('tupian1:{}'.format(duration[k]))
                video_writer.write(img1)
        else:
            for j in range(duration[k]):
                video_writer.write(img2)
    video_writer.release()
    return avi


jpg_become_avi(jpg=jpg, mov=mov)
