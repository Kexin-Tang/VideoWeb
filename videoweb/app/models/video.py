# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class VideoType(Enum):
    movie = "movie"
    cartoon = "cartoon"
    episode = "episode"
    talkshow = "talkshow"
    other = "other"

VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episode.label = '电视剧'
VideoType.talkshow.label = '真人秀'
VideoType.other.label = '其他'

class VideoSource(Enum):
    youtube = "youtube"
    bilibili = 'bilibili'
    custom = "custom"

VideoSource.youtube.label = 'Youtube'
VideoSource.bilibili.label = '哔哩哔哩'
VideoSource.custom.label = '自定义'

class Nation(Enum):
    china = "CHN"
    japan = "JPN"
    england = "UK"
    america = "US"
    other = "other"


class IdentityType(Enum):
    director = 'director'
    mainstar = 'mainstar'
    costar = 'costar'


IdentityType.mainstar.label = '主演'
IdentityType.costar.label = '配角'
IdentityType.director.label = '导演'


class Video(models.Model):
    user = models.ForeignKey(User, related_name='video', on_delete=models.CASCADE)
    videoName = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    videoType = models.CharField(max_length=50, default=VideoType.other.value)
    source = models.CharField(max_length=20, default=VideoSource.custom.value, null=False)
    nation = models.CharField(max_length=5, default=Nation.other.value)
    desc = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'videoName', 'videoType', 'source', 'nation')

    def __str__(self):
        return self.videoName

class VideoStar(models.Model):
    video = models.ForeignKey(Video, related_name='videoStar', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name

class VideoDetail(models.Model):
    video = models.ForeignKey(Video, related_name='videoDetail', on_delete=models.CASCADE)
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return '{} - {}'.format(self.video, self.number)



class CustomVideo(models.Model):
    video = models.ForeignKey(Video, related_name='customVideo', on_delete=models.CASCADE)
    public_id = models.CharField(max_length=100, null=False, default='')
    url = models.CharField(max_length=500, null=False)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        unique_together = ('video', 'public_id', 'name')




