import os
import subprocess
import glob
from jmgen import generate
# ####################
# 使用ffprobe指令，遍历同目录下所有文件，获取其分辨率、帧的数量和帧率
# 同时使用ffmpeg将所有文件转为YUV
# raw_mp4 = [f for f in os.listdir() if os.path.isfile(f)]
path = "/root/deepfake/"    #指定视频源文件（mp4）的目录
raw_mp4 = glob.glob(path + "*.mp4")
# 四个list分别记录视频名称、分辨率、帧数量和帧率
fileName    = []
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
    fileName.append((vid.rsplit('/',1)[1]).split('.')[0])    
    width.append(ret[0]) 
    height.append(ret[1])
    frameRate.append((ret[2].split('/'))[0])
    frameNumber.append(ret[3])

# 使用ffmpeg将视频转为YUV，若已转换完成，注释此节
for i in range(len(fileName)):
    cmd_yuv = "ffmpeg -i " + path + fileName[i] + ".mp4 -s " + width[i] + "x" + height[i] + " -pix_fmt yuv420p " + path + fileName[i] + ".yuv"
    os.system(cmd_yuv)

# 生成每个视频的JM编码器配置文件
shName = 'deepfake_JM.sh'      
shFile = open(shName, mode='w', encoding='utf-8')
for i in range(len(fileName)):
    generate(path, fileName[i], frameNumber[i], frameRate[i], width[i], height[i])
    shFile.write('./lencod.exe -f ' + fileName[i] + '.cfg > ' + fileName[i] + '.log &\n')
    if (i%60==0):
        shFile.write("wait\n")
shFile.write('wait\n')
shFile.close()
os.system('chmod 777 ' + shName)
