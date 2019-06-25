from django.db import models
"""
Create your models here.
작성자 : author
본문 : text
사진 : image
작성일 : created
수정일 : updated
+ tag, like, comment
"""
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model

from django.urls import reverse
# from storages.backends.s3boto3 import S3Boto3Storage


# reverse : urlpattern 이름을 가지고 주소를 만들어주는 함수

# User 모델은 확장이 가능하다
# 1. setting.AUTH_USER_MODEL
# 2. from django.contrib.auth import get_user_model
# from django.contrib.auth import get_user_model
class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    # author = models.ForeignKey(get_user_model())

    # pk는 데이터가 작기 때문에 사용된다
    # pk는 indexing이 걸려있기 때문에 검색이 빠르다

    # CASCADE : 연속해서 삭제 -> User(model)이 삭제 될 경우 내용도 함께 삭제한다
    # PROTECT : 내용이 모두 삭제되어야 User가 삭제될 수 있다
    #   탈퇴 프로세스에 사진을 우선 삭제하고 탈퇴 시킨다
    # 특정 셋팅

    # related_name으로 연관 데이터를 얻을 수 없다면 쿼리를 별도로 실행해야 한다.
    #   -> 내 프로필에서는 내가 올린 사진만 뜬다.

    text = models.TextField(blank=True)  # 필수 필드가 아니기 때문에 blank=True
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    # upload_to는 함수를 사용해서 폴더를 동적으로 설정할 수 있다.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        return reverse('photo:detail', args=[self.id])

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     # save 하기전에 실행
    #     super(Photo, self).delete(...)
    #     # save 한 후에 실행
    #
    # def delete(self, using=None, keep_parents=False):
    #     # before
    #     super(Photo, self).delete(...)
    #     # after
