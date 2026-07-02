from django.contrib import admin
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from ckeditor.widgets import CKEditorWidget

from .models import Announcement, Event, EventImage, EventQuote, EventSection, GalleryImage, HeroSlide, News, Page, SiteSetting, Sponsor, Story, TeamMember

RICH_TEXT = {models.TextField: {'widget': CKEditorWidget}}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'is_published')
    list_filter = ('is_published', 'date')
    list_editable = ('is_published',)
    search_fields = ('title_en', 'title_ar')
    date_hierarchy = 'date'
    fields = ('title_ar', 'title_en', 'content_ar', 'content_en', 'image', 'is_published')
    formfield_overrides = RICH_TEXT


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'is_published')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('title_en', 'title_ar')
    date_hierarchy = 'date'
    fields = ('title_ar', 'title_en', 'content_ar', 'content_en', 'image', 'is_published')
    formfield_overrides = RICH_TEXT


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category')
    list_filter = ('category',)
    search_fields = ('title_en', 'title_ar')
    fields = ('title_ar', 'title_en', 'image', 'category')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date')
    search_fields = ('member_name_en', 'member_name_ar')
    date_hierarchy = 'date'
    fields = ('member_name_ar', 'member_name_en', 'content_ar', 'content_en', 'image')
    formfield_overrides = RICH_TEXT


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'role_en', 'category')
    list_filter = ('category',)
    search_fields = ('name_en', 'name_ar', 'role_en', 'role_ar')
    fields = ('name_ar', 'name_en', 'role_ar', 'role_en', 'bio_ar', 'bio_en', 'image', 'category')


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active',)
    fieldsets = [
        ('Content', {'fields': [
            ('title_ar',    'title_en'),
            ('subtitle_ar', 'subtitle_en'),
            'image',
        ]}),
        ('Button 1', {'fields': [('cta1_text_ar', 'cta1_text_en'), 'cta1_url'], 'classes': ['collapse']}),
        ('Button 2', {'fields': [('cta2_text_ar', 'cta2_text_en'), 'cta2_url'], 'classes': ['collapse']}),
        ('Display',  {'fields': [('order', 'is_active')]}),
    ]


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('📊 Stats Bar — Home Page', {
            'description': 'The four numbers shown in the blue bar below the hero.',
            'fields': [
                ('stat1_number', 'stat1_label_ar', 'stat1_label_en'),
                ('stat2_number', 'stat2_label_ar', 'stat2_label_en'),
                ('stat3_number', 'stat3_label_ar', 'stat3_label_en'),
                ('stat4_number', 'stat4_label_ar', 'stat4_label_en'),
            ],
        }),
        ('📝 Footer — Description', {
            'description': 'Short paragraph shown under the LRC name in the footer.',
            'fields': [
                'footer_desc_ar',
                'footer_desc_en',
            ],
        }),
        ('🔗 Footer — Social Media', {
            'description': 'Paste the full URL for each platform. Leave blank to hide the icon.',
            'fields': [
                'facebook_url',
                'instagram_url',
                'youtube_url',
                'linkedin_url',
            ],
        }),
        ('📍 Footer — Contact Information', {
            'description': 'Shown in the Contact column at the bottom of every page.',
            'fields': [
                ('contact_address_ar', 'contact_address_en'),
                'contact_email',
                'contact_phone',
            ],
        }),
    ]

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSetting.objects.get_or_create(pk=1)
        return HttpResponseRedirect(reverse('admin:main_sitesetting_change', args=[obj.pk]))


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'show_in_nav', 'nav_order', 'is_published')
    list_editable = ('show_in_nav', 'nav_order', 'is_published')
    list_filter = ('show_in_nav', 'is_published')
    search_fields = ('title_en', 'title_ar')
    prepopulated_fields = {'slug': ('title_en',)}
    fields = (
        'title_ar', 'title_en',
        'content_ar', 'content_en',
        'banner_image',
        'slug',
        'show_in_nav', 'nav_order',
        'is_published',
    )
    formfield_overrides = RICH_TEXT


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    fields = ('name', 'logo', 'url', 'order')


class EventSectionInline(admin.StackedInline):
    model = EventSection
    extra = 1
    fields = (('title_ar', 'title_en'), 'content_ar', 'content_en', ('icon', 'order'))
    formfield_overrides = RICH_TEXT


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


class EventQuoteInline(admin.TabularInline):
    model = EventQuote
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'is_published')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('title_en', 'title_ar')
    prepopulated_fields = {'slug': ('title_en',)}
    inlines = [EventImageInline, EventSectionInline, EventQuoteInline]
    filter_horizontal = ('sponsors',)
    fieldsets = [
        ('Content', {'fields': [
            ('title_ar', 'title_en'),
            ('subtitle_ar', 'subtitle_en'),
            'content_ar', 'content_en',
        ]}),
        ('Stats Bar', {'fields': [
            ('stat1_number', 'stat1_label_ar', 'stat1_label_en'),
            ('stat2_number', 'stat2_label_ar', 'stat2_label_en'),
            ('stat3_number', 'stat3_label_ar', 'stat3_label_en'),
            ('stat4_number', 'stat4_label_ar', 'stat4_label_en'),
        ], 'classes': ['collapse']}),
        ('Settings', {'fields': ['date', 'slug', 'is_published']}),
        ('Sponsors', {'fields': ['sponsors']}),
    ]
    formfield_overrides = RICH_TEXT
