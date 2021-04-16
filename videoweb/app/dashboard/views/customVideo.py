from django.shortcuts import render, redirect, reverse
from app.dashboardModels.video import Video
from django.views.generic import View

class ListCustomVideo(View):
    TEMPLATE = 'dashboard'