from django.shortcuts import render, redirect, reverse
from app.dashboardModels.video import Video
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.dashboard.utils.permission import dashboardAuth
from app.dashboardModels.video import VideoType, VideoSource, Nation, Video, VideoStar, IdentityType, VideoDetail
from app.dashboard.utils.common import checkEnum
from django.contrib.auth.models import User


'''
    列出所有的视频简介内容
'''
class ListCustomVideo(View):
    TEMPLATE = 'dashboard/customVideo/listCustomVideo.html'

    @dashboardAuth
    def get(self, req):
        data = {}

        # 获取用户信息
        user = req.user
        data['user'] = user.username

        # 获取错误信息，设置error
        error = req.GET.get('error', '')
        data['error'] = error

        # 获取"用户自定义"视频的QueryList
        if user.is_superuser:
            videos = Video.objects.filter(source=VideoSource.custom.value)
        else:
            videos = Video.objects.filter(source=VideoSource.custom.value, user=user)
        data['videos'] = videos

        return render_to_response(req, self.TEMPLATE, data=data)

    @dashboardAuth
    def post(self, req):
        # 获取信息
        videoName = req.POST.get('videoName')
        image = req.POST.get('image')
        videoType = req.POST.get('videoType')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        user = req.user

        # 如果有该填写的区域为空
        if not all([videoName, image, videoType, nation, desc]):
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '请确保所有内容均被正确填写'))

        # 如果枚举类型错误
        if not checkEnum([VideoType, Nation], [videoType, nation]):
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '国家或视频源选择错误'))

        # 都无问题后存入DB
        video = Video(
            user=user,
            videoName=videoName,
            image=image,
            videoType=videoType,
            source='custom',
            nation=nation,
            desc=desc
        )
        video.save()

        return redirect(reverse('list_custom_video'))



'''
    编辑某个特定的视频
'''
class CustomEditVideo(View):
    TEMPLATE = 'dashboard/customVideo/editVideo.html'

    @dashboardAuth
    def get(self, req, id):
        data = {}
        video = Video.objects.get(id=id)
        error = req.GET.get('error', '')
        data['video'] = video
        data['error'] = error

        return render_to_response(req, self.TEMPLATE, data=data)


    def post(self, req, id):
        videoName = req.POST.get('videoName')
        image = req.POST.get('image')
        videoType = req.POST.get('videoType')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        if not all([videoName, image, videoType, nation, desc]):
            return redirect('{}?error={}'.format(reverse('external_video_edit', kwargs={'id': id}), '请确保所有内容均被正确填写'))

        if not checkEnum([VideoType, Nation], [videoType, nation]):
            return redirect('{}?error={}'.format(reverse('external_video_edit', kwargs={'id': id}), '种类、国家或视频源选择错误'))

        Video.objects.filter(pk=id).update(
            videoName=videoName,
            image=image,
            videoType=videoType,
            nation=nation,
            desc=desc
        )

        return redirect(reverse('list_custom_video'))



'''
    查看视频的详细信息
'''
class CustomVideoDetail(View):
    TEMPLATE = 'dashboard/customVideo/videoDetail.html'

    @dashboardAuth
    def get(self, req, id):
        data = {}

        # 获取视频
        exists = Video.objects.filter(id=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '没有该视频'))
        video = Video.objects.get(id=id)

        # 如果别的用户通过url强行访问别人的视频
        if str(req.user.username) != str(video.user):
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '您没有该视频内容或权限'))

        data['video'] = video

        # 查看视频相关的细节
        exists = VideoDetail.objects.filter(video=video).exists()
        if not exists:
            data['detail'] = ''
        else:
            detail = VideoDetail.objects.filter(video=video)
            data['detail'] = detail

        return render_to_response(req, self.TEMPLATE, data=data)

    @dashboardAuth
    def post(self, req, id):
        return render_to_response(req, self.TEMPLATE)


class CustomVideoSub(View):
    TEMPLATE = 'dashboard/customVideo/videoSub.html'

    @dashboardAuth
    def get(self, req, id):
        data = {}
        error = req.GET.get('error', '')
        data['error'] = error

        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return Http404()
        video = Video.objects.get(pk=id)
        details = VideoDetail.objects.filter(video=video)

        data['video'] = video
        data['details'] = details

        return render_to_response(req, self.TEMPLATE, data=data)



'''
    创建剧集
    @ TODO: 七牛云
'''
class AddCustomVideoSub(View):
    def post(self, req, id):
        url = req.POST.get('url', '')
        number = req.POST.get('number', '')
        if not all([url, number]):
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '请将“剧集”表单填写完整'))

        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '未找到该视频信息'))

        video = Video.objects.get(pk=id)
        exists = Detail.objects.filter(video=video, number=number).exists()
        # 如果该剧集已经被加入了
        if exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '该剧集已经被添加，请勿重复添加'))

        Detail.objects.create(video=video, url=url, number=number)
        return redirect(reverse('custom_videosub', kwargs={'id': id}))


'''
    删除剧集
    @ TODO: 七牛云
'''
class DeleteCustomVideoSub(View):
    def get(self, req, videoID, subID):
        exists = Video.objects.filter(pk=videoID).exists()
        if not exists:
            return Http404()

        exists = Detail.objects.filter(pk=subID).exists()
        if not exists:
            return Http404()

        Detail.objects.filter(pk=subID).delete()
        return redirect(reverse('custom_videosub', kwargs={'id': videoID}))


'''
    更新剧集
    @ TODO: 七牛云
'''
class UpdateCustomVideoSub(View):
    def post(self, req, id):
        number = req.POST.get('number', '')
        url = req.POST.get('url', '')
        subID = req.POST.get('id', '')

        if not all([number, url]):
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '请填写相应字段'))


        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '未找到对应的视频'))

        exists = Detail.objects.filter(pk=subID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '未找到对应的视频'))

        Detail.objects.filter(pk=subID).update(
            number=number,
            url=url
        )

        return redirect(reverse('custom_videosub', kwargs={'id': id}))