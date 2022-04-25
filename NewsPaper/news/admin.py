from django.contrib import admin
from .models import Category, Post, Comment, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'author')
    list_filter = ('author', 'category')
    search_fields = ('title', 'category__name_category')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)

