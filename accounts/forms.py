# model form : model, form(parent)
from django.contrib.auth.models import User
from django import forms


class SignUpForm(forms.ModelForm):
    # additional field password -> 우선순위가 더 높다
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User  # field password -> 우선순위가 낮다(생략되도 동작은 되나 순서가 마지막으로 변경됨)
        fields = ['first_name', 'last_name', 'username', 'password', 'password2']
        # fields의 순서는 html에 보여질 순서가 된다
        # fields = '__all__'
        # 추가 필드 -> 필드 목록과 추가 필드가 겹치면 오버라이드 된다(password)

    # clean_fieldname -> valid에 의해 실행됨
    def clean_password2(self):
        cd = self.cleaned_data  # fieldname(password2)의 index를 기준으로 앞에 해당하는 모든 field 값을 가져온다
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        # 규칙 : 해당 필드의 값을 리턴
        return cd['password2']
