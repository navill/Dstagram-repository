"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # 특정 리소스를 static형태로 응답
from django.conf import settings  # 장고의 셋팅값을 불러다 주는 역할


urlpatterns = [
    path('site_config/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('photo.urls'))
]






# image 출력을 위해 다음 urlpattern을 추가
# -> deploy, live일 때는 사용하지 않음
#   -> 장고에서 처리해야할 일이 아니기 때문에
# -> web server(heroku는 지원하지 않음)가 해주거나
# -> 파일 서버를 별도로 셋팅
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns