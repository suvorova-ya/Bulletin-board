from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from.models import Post,Author,Comment,Category




class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'is_published','cat', 'image')
    list_filter = ('is_published', 'cat', 'publish', 'author')
    search_fields = ('title', 'body','cat')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['is_published', 'publish']
    summernote_fields = ('body',)


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author', 'email', 'body')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}



admin.site.register(Author)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category,CategoryAdmin)