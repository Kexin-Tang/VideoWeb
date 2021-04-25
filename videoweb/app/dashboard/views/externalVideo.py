'''
    @ 用于处理外部链接视频的GET POST路由
'''
from django.views.generic import View
from django.shortcuts import redirect, render, reverse
from app.libs.base_render import render_to_response
from app.dashboard.utils.permission import dashboardAuth, checkLoginByCookies, checkLoginBySession
from app.models.video import VideoType, VideoSource, Nation, Video, VideoStar, IdentityType
from app.models.video import VideoDetail as Detail
from app.dashboard.utils.common import checkEnum
from django.http import Http404
from app.const.const import SESSION_NAME
from django.contrib.auth.models import User




'''
    视频主页，显示视频列表
'''
class ExternalVideo(View):
    TEMPLATE = 'dashboard/externalVideo/listExternalVideo.html'

    @checkLoginBySession
    def get(self, req):
        data = {}

        # 获取用户信息，如果是管理员，则设置user
        data['user'] = req.session.get('username', '')

        # 获取错误信息，设置error
        error = req.GET.get('error', '')
        data['error'] = error

        # 获取"非用户自定义"视频(即"外部链接"视频)的QueryList
        videos = Video.objects.exclude(source=VideoSource.custom.value)
        data['videos'] = videos

        return render_to_response(req, self.TEMPLATE, data=data)

    @checkLoginBySession
    def post(self, req):
        # 获取信息
        videoName = req.POST.get('videoName')
        image = req.POST.get('image')
        videoType = req.POST.get('videoType')
        videoSource = req.POST.get('videoSource')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        userID = req.session.get(SESSION_NAME)
        exists = User.objects.filter(pk=userID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('external_video'), '用户不存在'))

        user = User.objects.filter(pk=userID)[0]

        # 如果有该填写的区域为空
        if not all([videoName, image, videoType, videoSource, nation, desc]):
            return redirect('{}?error={}'.format(reverse('external_video'), '请确保所有内容均被正确填写'))

        # 如果枚举类型错误
        if not checkEnum([VideoType, VideoSource, Nation], [videoType, videoSource, nation]):
            return redirect('{}?error={}'.format(reverse('external_video'), '种类、国家或视频源选择错误'))

        # 都无问题后存入DB
        video = Video(
            user=user,
            videoName=videoName,
            image=image,
            videoType=videoType,
            source=videoSource,
            nation=nation,
            desc=desc
        )
        video.save()

        return redirect(reverse('external_video'))






'''
    显示某个视频的详细信息，如图片、简介、剧集等
'''
class VideoDetail(View):
    TEMPLATE = 'dashboard/externalVideo/videoDetail.html'

    @checkLoginBySession
    def get(self, req, id):
        data = {}

        # 获取视频
        exists = Video.objects.filter(id=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('external_video'), '没有该视频'))
        video = Video.objects.get(id=id)
        data['video'] = video

        # 查看视频相关的细节
        exists = Detail.objects.filter(video=video).exists()
        if not exists:
            data['detail'] = ''
        else:
            detail = Detail.objects.filter(video=video)
            data['detail'] = detail

        # 查看视频相关演员
        exists = VideoStar.objects.filter(video=video).exists()
        if not exists:
            data['stars'] = ''
        else:
            stars = VideoStar.objects.filter(video=video).order_by('identity')
            data['stars'] = stars
        return render_to_response(req, self.TEMPLATE, data=data)

    @checkLoginBySession
    def post(self, req, id):
        return render_to_response(req, self.TEMPLATE)






'''
    编辑某个特定的视频
'''
class EditVideo(View):
    TEMPLATE = 'dashboard/externalVideo/editVideo.html'

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
        videoSource = req.POST.get('videoSource')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        if not all([videoName, image, videoType, videoSource, nation, desc]):
            return redirect('{}?error={}'.format(reverse('external_video_edit', kwargs={'id': id}), '请确保所有内容均被正确填写'))

        if not checkEnum([VideoType, VideoSource, Nation], [videoType, videoSource, nation]):
            return redirect('{}?error={}'.format(reverse('external_video_edit', kwargs={'id': id}), '种类、国家或视频源选择错误'))

        Video.objects.filter(pk=id).update(
            videoName=videoName,
            image=image,
            videoType=videoType,
            source=videoSource,
            nation=nation,
            desc=desc
        )
        return redirect(reverse('external_video'))







'''
    查看视频详细的分集、演员等
'''
class VideoSubAndStarView(View):
    TEMPLATE = 'dashboard/externalVideo/videoSubStarView.html'

    @checkLoginBySession
    def get(self, req, id):
        data = {}
        error = req.GET.get('error', '')
        data['error'] = error

        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return Http404()
        video = Video.objects.get(pk=id)
        details = Detail.objects.filter(video=video)
        stars = VideoStar.objects.filter(video=video)

        data['video'] = video
        data['details'] = details
        data['stars'] = stars

        return render_to_response(req, self.TEMPLATE, data=data)







'''
    创建剧集
'''
class AddVideoSub(View):
    @checkLoginBySession
    def post(self, req, id):
        url = req.POST.get('url', '')
        number = req.POST.get('number', '')
        if not all([url, number]):
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '请将“剧集”表单填写完整'))

        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '未找到该视频信息'))

        video = Video.objects.get(pk=id)
        exists = Detail.objects.filter(video=video, number=number).exists()
        # 如果该剧集已经被加入了
        if exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '该剧集已经被添加，请勿重复添加'))

        Detail.objects.create(video=video, url=url, number=number)
        return redirect(reverse('video_sub_star_view', kwargs={'id': id}))








'''
    删除剧集
'''
class DeleteVideoSub(View):
    @checkLoginBySession
    def get(self, req, videoID, subID):
        exists = Video.objects.filter(pk=videoID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': videoID}), 'Not Found'))

        exists = Detail.objects.filter(pk=subID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': videoID}), 'Not Found'))

        Detail.objects.filter(pk=subID).delete()
        return redirect(reverse('video_sub_star_view', kwargs={'id': videoID}))








'''
    创建演员
'''
class AddVideoStar(View):
    @checkLoginBySession
    def post(self, req, id):
        name = req.POST.get('name', '')
        identity = req.POST.get('identity', '')
        if not all([name, identity]):
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '请将“演员”表单填写完整'))

        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '未找到该视频信息'))

        video = Video.objects.get(pk=id)
        exists = VideoStar.objects.filter(video=video, name=name, identity=identity).exists()
        # 如果该演员已经被加入了
        if exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '该演员已经被添加，请勿重复添加'))

        VideoStar.objects.create(video=video, name=name, identity=identity)
        return redirect(reverse('video_sub_star_view', kwargs={'id': id}))









'''
    删除演员
'''
class DeleteVideoStar(View):
    @checkLoginBySession
    def get(self, req, videoID, starID):
        exists = Video.objects.filter(pk=videoID).exists()
        if not exists:
            return Http404()

        exists = VideoStar.objects.filter(pk=starID).exists()
        if not exists:
            return Http404()

        VideoStar.objects.filter(pk=starID).delete()
        return redirect(reverse('video_sub_star_view', kwargs={'id': videoID}))








'''
    改变视频状态
'''
class ChangeStatus(View):
    @checkLoginBySession
    def get(self, req, id):
        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('external_video'), '未找到对应的视频'))

        video = Video.objects.get(pk=id)
        status = video.status
        status = False if status is True else True
        Video.objects.filter(pk=id).update(status=status)

        return redirect(reverse('external_video'))










'''
    修改剧集信息
'''
class UpdateVideoSub(View):
    @checkLoginBySession
    def post(self, req, id):
        number = req.POST.get('number', '')
        url = req.POST.get('url', '')
        subID = req.POST.get('id', '')

        if not all([number, url]):
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '请填写相应字段'))


        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '未找到对应的视频'))

        exists = Detail.objects.filter(pk=subID).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('video_sub_star_view', kwargs={'id': id}), '未找到对应的视频'))

        Detail.objects.filter(pk=subID).update(
            number=number,
            url=url
        )

        return redirect(reverse('video_sub_star_view', kwargs={'id': id}))