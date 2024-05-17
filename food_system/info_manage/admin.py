from django.contrib import admin
from django.utils.html import format_html

from .models import FoodModel, UserInfoModel, CategoryModel, HotModel, CommentModel, MarkModel, LikeModel


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'create_time')
    search_fields = ('username',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'view_count')

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="/image/{}" style="width:120px;height:70px;"/>'.format(obj.image))
        return ""

    image_tag.allow_tags = True
    image_tag.short_description = 'image'


class HotAdmin(admin.ModelAdmin):
    list_display = ('food',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'content', 'create_time')


class MarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'score', 'create_time')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'create_time')


admin.site.register(MarkModel, MarkAdmin)
admin.site.register(UserInfoModel, UserInfoAdmin)
admin.site.register(FoodModel, FoodAdmin)
admin.site.register(HotModel, HotAdmin)
admin.site.register(CommentModel, CommentAdmin)
admin.site.register(LikeModel, LikeAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.site_header = 'Deeper And Healthier'
