from django.urls import path
from app.dashboard.views.base import Index
from .views.auth import Login, Logout, AdminManage, UpdateAdminStatus

urlpatterns = [
    path('', Index.as_view(), name="dashboard_index"),
    path('login/', Login.as_view(), name="dashboard_login"),
    path('logout/', Logout.as_view(), name="dashboard_logout"),
    path('admin/manage', AdminManage.as_view(), name="admin_manage"),
    path('admin/manage/update/status', UpdateAdminStatus.as_view(), name="admin_update_status"),

]