from django.contrib import admin

# Register your models here.
from .models import Photo


# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'image', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['created', 'updated', 'text']
    ordering = ['-updated', '-created']
    raw_id_fields = ['author']  # select box에서 author의 id번호를 검색할 수 있도록 변경

admin.site.register(Photo, PhotoAdmin)
