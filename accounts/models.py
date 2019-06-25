from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Follow(models.Model):
    # 2개의 필드 - ForeignKey
    # A가 B를 팔로우 하고 있다(방향성)
    # on_delete -> 연관된 객체(User model의 한 객체와 연결된 데이터 포함)를 어떻게 삭제 할거냐?
    # related_name은 참조 객체의 입장에서 필드명, 속성값
    # a, b -> Follow object
    # a - me.id
    # b - you.id
    me = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    you = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    # foreignkey를 두개 사용할 경우 반드시 related_name 지정해야 에러없이 동작됨
    def __str__(self):
        return self.me.username + " follow " + self.you.username
