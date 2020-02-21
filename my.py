rtmpUrl = 'rtmp://127.0.0.1:1935/live'

camera = cv2.VideoCapture(0) # 从文件读取视频
#这里的摄像头可以在树莓派3b上使用
if (camera.isOpened()):# 判断视频是否打开 
    print 'Open camera'
else:
    print 'Fail to open camera!'
    return
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 2560x1920 2217x2217 2952×1944 1920x1080
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FPS, 5)


command = ['ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv', 
    rtmpUrl]
#管道特性配置
# pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
pipe = sp.Popen(command, stdin=sp.PIPE) #,shell=False
# pipe.stdin.write(frame.tostring())  


    # 绘制推送图片帧信息
    # print(len(faces))
    fpsshow = "Fps  :" + str(int(fps)) + "  Frame:" + str(count)  
    nframe  = "Play :" + str(int(count / fps))
    ntime   = "Time :" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if(count % fps == 0):
        print(fpsshow + " " + ntime)

    ############################图片输出
    # 结果帧处理 存入文件 / 推流 / ffmpeg 再处理
    pipe.stdin.write(frame.tostring())  # 存入管道用于直播
    out.write(frame)    #同时 存入视频文件 记录直播帧数据
    pass
camera.release()
# Release everything if job is finished
out.release()
print("Over!")
pass
