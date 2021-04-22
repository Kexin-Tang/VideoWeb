# coding:utf-8

import time
from config.celeryConfig import app
import os
import cloudinary.uploader
import cloudinary.api

from app.dashboardModels.video import CustomVideo

@app.task
def myUpload(filePath, public_id, newVideoID):
    res = cloudinary.uploader.upload(filePath, resource_type="video", public_id=public_id)
    targetURL = res['url']

    newVideo = CustomVideo.objects.get(pk=newVideoID)
    # 改变数据库内容，更新url
    newVideo.url = targetURL
    newVideo.save()

    removeFile(filePath)


@app.task
def myDelete(public_id):
    cloudinary.api.delete_resources(public_id, resource_type='video')


def removeFile(path):
    if os.path.exists(path):
        os.remove(path)