from django.shortcuts import render

# Create your views here.
"""
유저 목록이 출력되는 뷰
+기능 follow 기능
중간 테이블을 직접 생성 - 모델

유저 모델을 커스터마이징
확장하는법에 따라
1. 새로운 유저 모델 생성 - 기존 유저 데이터 유지 불가
2. 기존 모델 확장 - DB 다운 타임 alter table -> table lock
나의 유저 모델
나를 팔로우한 사람 필드
내가 팔로우한 사람 필드

커스터마이징을 할 수 없을 때
-> 새로운 모델을 추가하는 방법
many-to-many에 의해 자동으로 2개의 필드가 생성되지만, 안될 경우 
직접 many-to-many 필드 생성처럼 2개의 필드를 직접 생성한다

1. user 목록 혹은 유저 프로필에서 팔로우 버튼 생성
    1. 전체 유저 목록을 출력해주는 뷰 - 유저 모델에 대한 ListView
2. 팔로우 정보를 저장하는 뷰
"""
from django.views.generic.list import ListView
from django.views.generic.base import View

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .forms import SignUpForm


class UserListView(ListView):
    model = User
    template_name = "accounts/user_list.html"


# 기존의 뷰는 CreateView를 상속받기 때문에 상속이 어렵다
# 회원가입 -> 유저 모델값을 받는다 -> CreateView전달
# 회원 가입 시 모델 필드 외에 추가 입력이 요구됨
# 커스텀을 하려면 함수형 뷰가 적절하다

def signup(request):
    # class based view -> dispatch(get, post)
    if request.method == 'POST':
        # # original source for validation
        # username = request.POST.get('username')  # from singup.html
        # password = request.POST.get('password')  # Post 동작 시, get 함수를 이용해 변수명을 받는다
        # # password2 = request.POST.get('password2')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')

        # simple source for validation
        signup_form = SignUpForm(request.POST)
        # call validation
        if signup_form.is_valid():  # 회원가입이 정상적으로 처리 되었을 때, render 반환
            # - save and create instance
            user_instance = signup_form.save(commit=False)  # request.POST 기반 user_instance 생성
            # encode password
            # cleaned_data : data of valid text with filtering process
            # if using request.POST.get('password') -> non valid text
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()
            # username을 context를 이용해 signup_complete에 전달
            context_data = {}
            return render(request, 'accounts/signup_complete.html', {'username': user_instance.username})

        # 회원 객체 생성(User)
        # user = User()  # admin에 등록될 객체
        # user.username = username
        # user.first_name = first_name
        # user.last_name = last_name
        # # user.password = password
        # user.set_password(password)  # password 보안 처리
        # # valid = check_password(password, password2)
        # if not valid:
        #     raise user.DoesNotExist("Password Incorrect")
        # user.save()

        # edit source -> model form을 이용해 간결한 validation 구현
        # return render(request, 'accounts/signup_complete.html')

    else:
        # form : usernaem, password
        # form = SignUpForm()  # forms.py에서 작성된 form object
        # # render 동작
        # # 1. template 불러오기
        # # 2. 템플릿 렌더링하기 -> template rendering -> notion 참고
        # # 3. HTTP response하기
        # context_value = {'form': form}  # variable 전달
        # return render(request, 'accounts/signup.html', context_value)

        signup_form = SignUpForm()
    # return render의 위치를 변경함으로써, 잘못 입력 시 양식이 채워진채로 리로드 된다
    return render(request, 'accounts/signup.html', {'form': signup_form})


class UserFollowerList(ListView):
    model = User
    template_name = 'accounts/follower_list.html'


class UserFollowingList(ListView):
    model = User
    template_name = 'accounts/following_list.html'


class UserFollower(View):
    def get(self, request, *args, **kwargs):
        pass


class UserFollowing(View):
    def get(self, request, *args, **kwargs):
        pass
