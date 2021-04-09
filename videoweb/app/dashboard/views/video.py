from django.views.generic import View
from django.shortcuts import redirect, render, reverse
from app.libs.base_render import render_to_response
from app.dashboard.utils.permission import dashboardAuth
from app.dashboardModels.video import VideoType, VideoSource, Nation, Video
from app.dashboardModels.video import VideoDetail as Detail
from app.dashboard.utils.common import checkEnum

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

        Video.objects.create(
            videoName=videoName,
            image=image,
            videoType=videoType,
            source=videoSource,
            nation=nation,
            desc=desc
        )

        return redirect(reverse('external_video'))


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
            detail = Detail.objects.get(video=video)
            data['detail'] = detail

        return render_to_response(req, self.TEMPLATE, data=data)

class EditVideo(View):
    TEMPLATE = 'dashboard/video/editVideo.html'

    @dashboardAuth
    def get(self, req, id):
        data = {}
        video = Video.objects.get(id=id)
        data['video'] = video

        exists = Detail.objects.filter(video=video).exists()
        if not exists:
            data['detail'] = ''
        else:
            detail = Detail.objects.get(video=video)
            data['detail'] = detail

        return render_to_response(req, self.TEMPLATE, data=data)

    def post(self, req, id):
        pass