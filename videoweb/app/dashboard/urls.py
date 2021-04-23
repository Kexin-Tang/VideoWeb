from django.urls import path
from app.dashboard.views.base import Index
from .views.auth import Login, Logout, AdminManage, UpdateAdminStatus, Register
from .views.externalVideo import ExternalVideo, VideoDetail, EditVideo, VideoSubAndStarView, DeleteVideoSub, DeleteVideoStar, AddVideoStar, AddVideoSub, ChangeStatus, UpdateVideoSub
from .views.customVideo import ListCustomVideo, CustomEditVideo, CustomVideoDetail, CustomVideoSub, AddCustomVideoSub, DeleteCustomVideoSub, UpdateCustomVideoSub, PlayCustomVideo, checkStatus


urlpatterns = [
    path('', Index.as_view(), name="dashboard_index"),
    path('login/', Login.as_view(), name="dashboard_login"),
    path('logout/', Logout.as_view(), name="dashboard_logout"),
    path('register/', Register.as_view(), name='dashboard_register'),

    path('admin/manage', AdminManage.as_view(), name="admin_manage"),
    path('admin/manage/update/status', UpdateAdminStatus.as_view(), name="admin_update_status"),

    path('video/external', ExternalVideo.as_view(), name="external_video"),
    path('video/external/<int:id>', VideoDetail.as_view(), name='external_video_detail'),
    path('video/external/edit/<int:id>', EditVideo.as_view(), name='external_video_edit'),
    path('video/external/view/<int:id>', VideoSubAndStarView.as_view(), name='video_sub_star_view'),
    path('video/external/deletesub/<int:videoID>/<int:subID>', DeleteVideoSub.as_view(), name='delete_sub'),
    path('video/external/deletestar/<int:videoID>/<int:starID>', DeleteVideoStar.as_view(), name='delete_star'),
    path('video/external/addsub/<int:id>', AddVideoSub.as_view(), name='add_sub'),
    path('video/external/addstar/<int:id>', AddVideoStar.as_view(), name='add_star'),
    path('video/external/changestatus/<int:id>', ChangeStatus.as_view(), name='external_video_status'),
    path('video/external/updatesub/<int:id>', UpdateVideoSub.as_view(), name='update_sub'),

    path('video/custom', ListCustomVideo.as_view(), name="list_custom_video"),
    path('video/custom/<int:id>', CustomVideoDetail.as_view(), name="custom_video_detail"),
    path('video/custom/edit/<int:id>', CustomEditVideo.as_view(), name="custom_video_edit"),
    path('video/custom/view/<int:id>', CustomVideoSub.as_view(), name='custom_videosub'),
    path('video/custom/addsub/<int:id>', AddCustomVideoSub.as_view(), name='custom_videosub_add'),
    path('video/custom/deletesub/<int:videoID>/<int:subID>', DeleteCustomVideoSub.as_view(), name="custom_videosub_delete"),
    path('video/custom/updatesub/<int:id>', UpdateCustomVideoSub.as_view(), name="custom_videosub_update"),
    path('video/custom/play/<int:videoID>/<int:subID>', PlayCustomVideo.as_view(), name="custom_video_play"),

    path('check', checkStatus, name="checkStatus"),
]