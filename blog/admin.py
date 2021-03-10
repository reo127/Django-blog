from django.contrib import admin
from blog.models import Post, BlogComments

# Register your models here.

admin.site.register(( BlogComments))
# admin.site.register(( Post))

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     class media:
#         js = ('tinyinject.js')

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)