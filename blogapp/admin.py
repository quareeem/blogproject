from django.contrib import admin
from .models import Post, Comment, Category
from mptt.admin import MPTTModelAdmin


@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status')
    prepopulated_fields = {
        'slug': ('title',),
    }

admin.site.register(Category)
admin.site.register(Comment, MPTTModelAdmin)