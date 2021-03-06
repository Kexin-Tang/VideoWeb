from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from app.models.video import Video
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.dashboard.utils.permission import dashboardAuth, checkLoginBySession, checkLoginByCookies
from app.models.video import VideoType, VideoSource, Nation, Video, VideoStar, IdentityType, CustomVideo
from app.dashboard.utils.common import checkEnum, customVideoUpload, customVideoDelete
from django.contrib.auth.models import User
from celery.result import AsyncResult
from app.const.const import SESSION_NAME





'''
    列出所有的视频简介内容
'''
class ListCustomVideo(View):
    TEMPLATE = 'dashboard/customVideo/listCustomVideo.html'

    @checkLoginBySession
    def get(self, req):
        data = {}

        # 获取错误信息，设置error
        error = req.GET.get('error', '')
        data['error'] = error

        # 获取"用户自定义"视频的QueryList
        if (req.session.get('username') == 'admin'):
            videos = Video.objects.filter(source=VideoSource.custom.value)
        else:
            videos = Video.objects.filter(source=VideoSource.custom.value, user=user)
        data['videos'] = videos
        return render_to_response(req, self.TEMPLATE, data=data)


    @checkLoginBySession
    def post(self, req):
        # 获取信息
        videoName = req.POST.get('videoName')
        image = req.POST.get('image')
        videoType = req.POST.get('videoType')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        userID = req.session.get(SESSION_NAME)
        exists = User.objects.filter(pk=userID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '用户不存在'))
        user = User.objects.filter(pk=userID)[0]

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

    @checkLoginBySession
    def get(self, req, id):
        data = {}
        video = Video.objects.get(id=id)
        error = req.GET.get('error', '')
        data['video'] = video
        data['error'] = error
        return render_to_response(req, self.TEMPLATE, data=data)

    @checkLoginBySession
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

    @checkLoginBySession
    def get(self, req, id):
        data = {}

        # 获取视频
        exists = Video.objects.filter(id=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '没有该视频'))
        video = Video.objects.get(id=id)

        # 如果别的用户通过url强行访问别人的视频
        if (req.session.get('username')!='admin') and str(req.session.get('username')) != str(video.user):
            return redirect('{}?error={}'.format(reverse('list_custom_video'), '您没有该视频内容或权限'))

        data['video'] = video

        # 查看视频相关的细节
        exists = CustomVideo.objects.filter(video=video).exists()
        if not exists:
            data['detail'] = ''
        else:
            detail = CustomVideo.objects.filter(video=video)
            data['detail'] = detail
        return render_to_response(req, self.TEMPLATE, data=data)

    @checkLoginBySession
    def post(self, req, id):
        return render_to_response(req, self.TEMPLATE)





class CustomVideoSub(View):
    TEMPLATE = 'dashboard/customVideo/videoSub.html'

    @checkLoginBySession
    def get(self, req, id):
        data = {}
        error = req.GET.get('error', '')
        data['error'] = error

        # 获取异步消息队列的task_id
        task_id = req.GET.get('task_id', '')
        data['task_id'] = task_id

        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return Http404()
        video = Video.objects.get(pk=id)
        details = CustomVideo.objects.filter(video=video).order_by('public_id')

        data['video'] = video
        data['details'] = details

        return render_to_response(req, self.TEMPLATE, data=data)



'''
    创建剧集
'''
class AddCustomVideoSub(View):
    @checkLoginBySession
    def post(self, req, id):
        file = req.FILES.get('url', '')
        name = req.POST.get('name', '')
        if not all([file, name]):
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '请将“剧集”表单填写完整'))

        # 判断用户点击的视频是否存在
        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '未找到该视频信息'))

        # 找到对应的视频，查看当前添加的集数是否已经存在
        video = Video.objects.get(pk=id)
        exists = CustomVideo.objects.filter(video=video, name=name).exists()
        # 如果该剧集已经被加入了
        if exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '该剧集已经被添加，请勿重复添加'))

        task_id = customVideoUpload(file, video, name)    # 负责上传内容至云端，并保存入数据库

        return redirect('{}?task_id={}'.format(reverse('custom_videosub', kwargs={'id': id}), task_id))



'''
    预览与播放上传的视频
'''
class PlayCustomVideo(View):
    TEMPLATE = 'dashboard/customVideo/playVideo.html'

    @checkLoginBySession
    def get(self, req, videoID, subID):
        data = {}

        exists = Video.objects.filter(pk=videoID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': videoID}), 'Not Found'))

        exists = CustomVideo.objects.filter(pk=subID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': videoID}), 'Not Found'))

        data['url'] = CustomVideo.objects.get(pk=subID).url
        data['id'] = videoID
        return render_to_response(req, self.TEMPLATE, data=data)

'''
    删除剧集
'''
class DeleteCustomVideoSub(View):
    @checkLoginBySession
    def get(self, req, videoID, subID):
        exists = Video.objects.filter(pk=videoID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': videoID}), 'Not Found'))

        exists = CustomVideo.objects.filter(pk=subID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': videoID}), 'Not Found'))

        video = CustomVideo.objects.get(pk=subID)
        customVideoDelete(video.public_id)              # 删除云端视频
        CustomVideo.objects.filter(pk=subID).delete()   # 删除数据库内容
        return redirect(reverse('custom_videosub', kwargs={'id': videoID}))


'''
    更新剧集
'''
class UpdateCustomVideoSub(View):
    @checkLoginBySession
    def post(self, req, id):
        name = req.POST.get('name', '')
        subID = req.POST.get('id', '')

        if not all([name]):
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '请填写相应字段'))


        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '未找到对应的视频'))

        exists = CustomVideo.objects.filter(pk=subID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('custom_videosub', kwargs={'id': id}), '未找到对应的视频'))

        CustomVideo.objects.filter(pk=subID).update(
            name=name,
        )

        return redirect(reverse('custom_videosub', kwargs={'id': id}))


def checkStatus(req):
    task_id = req.GET.get('task_id')
    if task_id:
        async_result = AsyncResult(task_id)
        return JsonResponse({'status': async_result.ready()})
    return JsonResponse({'status': False})
