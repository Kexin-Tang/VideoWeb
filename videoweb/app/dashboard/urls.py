from django.urls import path
from app.dashboard.views.base import Index
from .views.auth import Login, Logout, AdminManage, UpdateAdminStatus
from .views.video import ExternalVideo, VideoDetail, EditVideo, VideoSubAndStarView, DeleteVideoSub, DeleteVideoStar, AddVideoStar, AddVideoSub

urlpatterns = [
    path('', Index.as_view(), name="dashboard_index"),
    path('login/', Login.as_view(), name="dashboard_login"),
    path('logout/', Logout.as_view(), name="dashboard_logout"),
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
]