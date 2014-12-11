from django.contrib import admin
from models import *


class WebPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True

    fieldsets = (
        ('General Info', {
            'fields': ('title', 'slug', 'template_override', 'chart_title', 'is_active')
        }),
        ('Totals By Source', {
            'classes': ('full-width',),
            'fields': ('content',)
        }),
    )

    class Media:
        js = [
            '/static/admin_js/tinymce/tinymce.min.js',
            '/static/admin_js/tinymce_init.js'
        ]


class InlineSublink(admin.TabularInline):
    model = HeaderSubLink


class HeaderLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order',)
    inlines = [
        InlineSublink,
    ]

    class Media:
        js = [
            '/static/admin_js/tinymce/tinymce.min.js',
            '/static/admin_js/tinymce_init.js'
        ]


class HomePage_SectionAdmin(admin.ModelAdmin):
    list_display = ('sect_type',)

    class Media:
        js = [
            '/static/admin_js/tinymce/tinymce.min.js',
            '/static/admin_js/tinymce_init.js'
        ]


admin.site.register(WebPage, WebPageAdmin)
admin.site.register(HeaderLink, HeaderLinkAdmin)
admin.site.register(HomePage_Section, HomePage_SectionAdmin)