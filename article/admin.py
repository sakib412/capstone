from django.contrib import admin
from .models import Category,Post,Comment,UserExtended
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserExtendedInline(admin.StackedInline):
    model = UserExtended
    can_delete = False
    verbose_name = 'user'
    verbose_name_plural = 'users'


class UserAdmin(BaseUserAdmin):
    inlines = (UserExtendedInline, )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_slug',)
    search_fields = ('category_slug',)
    prepopulated_fields = {'category_slug': ('category_name',)}

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','category', 'status','created_on')
    list_filter = ("status","author","updated_on","category")
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'updated_on', 'active')
    list_filter = ('active', 'updated_on', 'created_on')
    search_fields = ('name', )
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)