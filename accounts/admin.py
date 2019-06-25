from django.contrib import admin
from .models import Follow


class FollowOption(admin.ModelAdmin):
    list_display = ['id', 'me', 'you']
    # list_filter = ['me']
    # search_fields = ['me', 'your']
    # ordering = ['me']
    raw_id_fields = ['me', 'you']  # select box에서 author의 id번호를 검색할 수 있도록 변경


admin.site.register(Follow, FollowOption)
