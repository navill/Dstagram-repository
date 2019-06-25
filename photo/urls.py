from django.urls import path
from .views import *

app_name = 'photo'

urlpatterns = [
    path('', PhotoListView.as_view(), name='index'),
    path('create/', PhotoCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PhotoUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', PhotoDetailView.as_view(), name='detail'),


    path('like/', PhotoLikeList.as_view(), name='like_list'),
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('favorite/', PhotoSaveList.as_view(), name='save_list'),
    path('favorite/<int:photo_id>/', PhotoSave.as_view(), name='favorite'),
]


