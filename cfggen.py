import os
import subprocess
import glob
# ####################
# 使用ffprobe指令，遍历同目录下所有文件，获取其分辨率、帧的数量和帧率
# 同时使用ffmpeg将所有文件转为YUV
# raw_mp4 = [f for f in os.listdir() if os.path.isfile(f)]
path = "/root/deepfakees/"    #指定视频源文件（mp4）的目录
raw_mp4 = glob.glob(path + "*.mp4")
# 四个list分别记录视频路径、分辨率、帧数量和帧率
filePath    = []
width       = []
height      = []
frameNumber = []
frameRate   = []
for vid in raw_mp4:
    # 对每个mp4视频执行ffprobe指令
    cmd = "ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,width,height,r_frame_rate -of default=nokey=1:noprint_wrappers=1 " + vid
    ret = subprocess.getoutput(cmd).split()
    print(vid, ret)         #输出ffprobe得到的信息
    # 记录ffprobe输出信息
    filePath.append(vid)    
    width.append(ret[0]) 
    height.append(ret[1])
    frameRate.append(ret[2].split('/'))
    frameNumber.append(ret[3])
