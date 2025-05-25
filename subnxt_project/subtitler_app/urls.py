from django.urls import path
from . import views

app_name = 'subtitler_app'  # Good practice for namespacing URLs

urlpatterns = [
    path('', views.index_view, name='index'),
    path('process/', views.process_video_view, name='process_video'),
]
