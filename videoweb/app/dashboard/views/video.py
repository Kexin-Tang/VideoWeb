from django.views.generic import View
from django.shortcuts import redirect, render, reverse
from app.libs.base_render import render_to_response
from app.dashboard.utils.permission import dashboardAuth
from app.dashboardModels.video import VideoType, VideoSource, Nation, Video, VideoStar
from app.dashboardModels.video import VideoDetail as Detail
from app.dashboard.utils.common import checkEnum
from django.http import Http404

'''
    视频主页，显示视频列表
'''
class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/externalVideo.html'

    @dashboardAuth
    def get(self, req):
        error = req.GET.get('error', '')
        videos = Video.objects.exclude(source=VideoSource.custom.value)
        data = {'error': error, 'videos': videos}
        return render_to_response(req, self.TEMPLATE, data=data)

    def post(self, req):
        videoName = req.POST.get('videoName')
        image = req.POST.get('image')
        videoType = req.POST.get('videoType')
        videoSource = req.POST.get('videoSource')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        if not all([videoName, image, videoType, videoSource, nation, desc]):
            return redirect('{}?error={}'.format(reverse('external_video'), '请确保所有内容均被正确填写'))

        if not checkEnum([VideoType, VideoSource, Nation], [videoType, videoSource, nation]):
            return redirect('{}?error={}'.format(reverse('external_video'), '种类、国家或视频源选择错误'))

        video = Video(
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
    TEMPLATE = 'dashboard/video/videoDetail.html'

    @dashboardAuth
    def get(self, req, id):
        data = {}
        video = Video.objects.get(id=id)
        data['video'] = video

        exists = Detail.objects.filter(video=video).exists()
        if not exists:
            data['detail'] = ''
        else:
            detail = Detail.objects.filter(video=video)
            data['detail'] = detail

        return render_to_response(req, self.TEMPLATE, data=data)

    @dashboardAuth
    def post(self, req, id):
        return render_to_response(req, self.TEMPLATE)

'''
    编辑某个特定的视频
'''
class EditVideo(View):
    TEMPLATE = 'dashboard/video/editVideo.html'

    @dashboardAuth
    def get(self, req, id):
        data = {}
        video = Video.objects.get(id=id)
        error = req.GET.get('error', '')
        data['video'] = video
        data['error'] = error

        return render_to_response(req, self.TEMPLATE, data=data)


    def post(self, req, id):
        image = req.POST.get('image')
        videoType = req.POST.get('videoType')
        videoSource = req.POST.get('videoSource')
        nation = req.POST.get('nation')
        desc = req.POST.get('desc')

        if not all([image, videoType, videoSource, nation, desc]):
            return redirect('{}?error={}'.format(reverse('external_video_edit', kwargs={'id': id}), '请确保所有内容均被正确填写'))

        if not checkEnum([VideoType, VideoSource, Nation], [videoType, videoSource, nation]):
            return redirect('{}?error={}'.format(reverse('external_video_edit', kwargs={'id': id}), '种类、国家或视频源选择错误'))

        Video.objects.filter(pk=id).update(
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
    TEMPLATE = 'dashboard/video/videoSubStarView.html'

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
    def get(self, req, videoID, subID):
        exists = Video.objects.filter(pk=videoID).exists()
        if not exists:
            return Http404()

        exists = Detail.objects.filter(pk=subID).exists()
        if not exists:
            return Http404()

        Detail.objects.filter(pk=subID).delete()
        return redirect(reverse('video_sub_star_view', kwargs={'id': videoID}))


'''
    创建演员
'''
class AddVideoStar(View):
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
    def get(self, req, id):
        exists = Video.objects.filter(pk=id).exists()
        if not exists:
            return redirect('{}?error={}'.format(reverse('external_video'), '未找到对应的视频'))

        video = Video.objects.get(pk=id)
        status = video.status
        status = False if status is True else True
        Video.objects.filter(pk=id).update(status=status)

        return redirect(reverse('external_video'))