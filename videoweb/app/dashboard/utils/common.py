from config import settings
import os
import time

import cloudinary
import cloudinary.uploader
import cloudinary.api

from app.tasks.task import myUpload, myDelete
from app.dashboardModels.video import CustomVideo

'''
    用于检测枚举类型是否正确
'''
def checkEnum(enumList, inputList):
    try:
        n = len(enumList)
        for i in range(n):
            enumList[i](inputList[i])
    except:
        return False
    return True


'''
    用于让用户上传视频到cloudinary
'''
def customVideoUpload(file, video, name):

    BASE_PATH = settings.BASE_DIR
    storeFolder = os.path.join(BASE_PATH, 'app/temp')

    videoFile = file.name
    videoFile = videoFile.replace(' ', '_')                         # 去掉文件名中的空格
    videoFile = '{}_{}'.format(int(time.time()), videoFile)         # 加上时间戳
    public_id = '{}/{}'.format(settings.cloudinary_file, os.path.splitext(videoFile)[0]) # 获取cloudinary中存储的名字

    # 将视频存储到temp
    transformFile = os.path.join(storeFolder, videoFile)
    with open(transformFile, 'wb') as f:
        for content in file.chunks():
            f.write(content)

    # 先创建内容，保证前端能预览，之后再更新url即可
    newVideo = CustomVideo.objects.create(
        video=video,
        url='',
        public_id=public_id,
        name=name
    )

    # 异步队列
    task = myUpload.delay(transformFile, public_id, newVideo.id)
    return task.id


'''
    让用户删除clodinary指定的视频
'''
def customVideoDelete(public_id):
    public_id = [public_id]     # 注意，public_id需要是一个 list
    myDelete.delay(public_id)

