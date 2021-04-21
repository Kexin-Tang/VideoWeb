from config import settings
import os
import time

import cloudinary
import cloudinary.uploader
import cloudinary.api

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
def customVideoUpload(video):
    videoFile = video.name
    videoFile = videoFile.replace(' ', '_')                         # 去掉文件名中的空格
    videoFile = os.path.splitext(videoFile)[0]                      # 去掉文件类型
    videoFile = '{}_{}'.format(int(time.time()), videoFile)         # 加上时间戳
    public_id = '{}/{}'.format(settings.cloudinary_file, videoFile) # 获取cloudinary中存储的名字

    res = cloudinary.uploader.upload(video, resource_type = "video", public_id=public_id)
    return res


'''
    让用户删除clodinary指定的视频
'''
def customVideoDelete(public_id):
    public_id = [public_id]     # 注意，public_id需要是一个 list
    cloudinary.api.delete_resources(public_id, resource_type='video')

