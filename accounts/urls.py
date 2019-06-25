from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserListView
from .views import signup, UserFollowingList, UserFollowerList


app_name = 'accounts'
urlpatterns = [
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('signup.html/', signup, name='signup'),
    path('signup_complete.html/', signup, name='signup_complete'),
    path('user/followerlist/', UserFollowerList.as_view(), name='follower_list'),
    path('user/followinglist/', UserFollowingList.as_view(), name='following_list'),
]
