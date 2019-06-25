from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.http import HttpResponseRedirect
from django.contrib import messages
from photo.models import Photo

# Create your views here.
# CRUDL - image
# 쿼리셋 변경, context_data 추가, 권한 체크
# 함수형 뷰 <-> 제네릭 뷰
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


# mixin : 클래스형 뷰
# decorator : 함수형 뷰
# 뷰를 실행하기전에 특정한 로직을 추가로 실행해야할 경우 사용됨
# -> 로그인 여부, csrf 체크 수행 여부


# login, logout은 view 상속 받지 않고 urls에서 template 관련 설정할 수 있다
class PhotoListView(LoginRequiredMixin, ListView):
    # 로그인 여부는 자동으로 체크 -> 로그인이 성공할 경우만 실행
    # setting.py에 필드 추가
    model = Photo
    template_name = "photo/photo_list.html"


class PhotoLikeList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "photo/photo_list.html"

    def get_queryset(self):
        # 로그인한 유저가 좋아요를 클릭한 글을 찾아서 반환
        # 기존 -> photo.like.all()을 이용해 좋아요를 누른 사람을 찾는다
        # model-> related_name= like_post
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class PhotoSaveList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "photo/photo_list.html"

    def get_queryset(self):
        # 로그인한 유저가 좋아요를 클릭한 글을 찾아서 반환
        # 기존 -> photo.like.all()을 이용해 좋아요를 누른 사람을 찾는다
        # model-> related_name= like_post
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset


class PhotoCreateView(CreateView):
    model = Photo
    fields = ['image', 'text']
    template_name = "photo/photo_create.html"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context_data = super(PhotoCreateView, self).get_context_data(**kwargs)
        context_data['writer'] = self.request.user.username
        return context_data

    def form_valid(self, form):
        # author_id에 작성자를 연결
        form.instance.author_id = self.request.user.id
        # 입력된 자료가 올바른지 체크
        if form.is_valid():  # 올바를 경우
            # form : model form from 'model = Photo'
            form.instance.save()
            # media_model.save()
            return redirect('/')
            # foreign key일 경우 fieldname_id로 자동 생성 된다
        else:  # 올바르지 않을 경우
            return self.render_to_response({'form': form})


class PhotoUpdateView(UpdateView):
    model = Photo
    fields = ['image', 'text']
    template_name = "photo/photo_update.html"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()  # object : class 내의 model(Photo object)를 얻는다
        if object.author != request.user:  # request.user : web browser에서 전달할 때 포함한 유저 정보를 받는다
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoUpdateView, self).dispatch(request, *args, **kwargs)  # from base.py View.dispatch()
            # self : model = Photo -> dispatch([from User])
            # dispatch를 통해 self(model)에 handler(수정사항을 포함)를 리턴


class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = "photo/photo_delete.html"
    success_url = '/'

    # framework는 라이프 사이클이 존재 : 어떤 순서로 구동이 되느냐?
    # urlconf -> view -> model(db가 사용될 경우)
    # 아래의 함수는 뷰를 구동할 때 동작하는 순서
    # 
    # 사용자가 접속했을 때, get인지 post인지 결정하고 분기
    # --> 아래의 각 단계에서 권한에 대한 분기를 결정할 수 있다
    #       --> 본 예제에서는 get를 이용하여 권한 부여
    # -> dispatch를 사용할 경우 get, post 두개를 이용하지 않아도 된다
    # -> 상황에 따라 dispatch vs get, post
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDeleteView, self).dispatch(request, *args, **kwargs)

    # # 로직 수행, 템플릿 렌더링
    # def get(self, request, *args, **kwargs):  # get, post는 하나의 셋트
    #     object = self.get_object()
    #     if object.author != request.user:
    #         # 1. 삭제 페이지에서 권한이 없다!
    #         # 2. detail page로 돌아가서 삭제에 실패 했습니다!
    #         # 버튼이 없다고 실행하지 못하는 것은 아니기 때문에(주소로 접근) 접근을 back-end에서 직접 제한해야한다.
    #         # messgaes from settings.py in TEMPLATES = 'django.contrib.messages.context_processors.messages',
    #         messages.warning(request, "삭제할 권한이 없습니다.")
    #         # messages.error(), success() 등 다양하게 수정할 수 있음
    #
    #         return HttpResponseRedirect(object.get_absolute_url())
    #     else:  # 정상적인 상황
    #         return super(PhotoDeleteView, self).get(request, args, kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     if object.author != request.user:
    #         messages.warning(request, "삭제할 권한이 없습니다.")
    #         return HttpResponseRedirect(object.get_absolute_url())
    #     else:
    #         return super(PhotoDeleteView, self).post(request, args, kwargs)
    #
    # # 해당 쿼리셋을 이용해 현재 페이지에 필요한 object를 인스턴스화
    # def get_object(self, queryset=None):
    #     pass
    #
    # # 어떻게 데이터를 가져올 것인지?
    # def get_queryset(self):
    #     pass


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'


# url연결 + 템플릿은 없어도 된다
class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        # like 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseForbidden('/accounts/signin')
        else:
            # 1. 어떤 포스팅?
            # url: www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # url: www.naver.com/blog/like/1
            # path('blog/like/<int:photo_id>/')
            # kwargs['photo_id']
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():  # unlike
                    photo.like.remove(user)
                else:
                    photo.like.add(user)  # like
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PhotoSave(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():  # unlike
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)  # like
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
            # return HttpResponseRedirect('/')


from django.db.models.signals import post_delete
from django.dispatch import receiver  # receiver : signal 발생 확인


# @receiver(signal, signalfrom)  sender=model model에서 발생한 signal 처리
@receiver(post_delete, sender=Photo)
def post_delete(sender, instance, **kwargs):
    # local에서 다음 명령이 적용가능하지만, s3경우 절대경로를 지원하지 않기 때문에 다음과 같은 명령은 실행할 수 없다
    # local path: media/timeline_photo/...
    storage = instance.image.storage
    if storage.exists(str(instance.image)):
        storage.delete(str(instance.image))
        print(instance)

    # # s3연결 -> 사진 Object 삭제
    # session = boto3.Session(
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #     region_name=settings.AWS_REGION
    # )
    # s3 = session.resource('s3')
    # # image = s3.Object()
    # # s3.Object는 s3에 업로드된 파일 객체를 얻어오는 클래스
    # # arg1 = bucket name
    # # arg2 = file path(s3에서는 key)
    # image = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'media/'+str(instance.image))
    # image.delete()
