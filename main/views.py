from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Announcement, GalleryImage, HeroSlide, News, Page, SiteSetting, Story, TeamMember


def home(request):
    context = {
        'hero_slides':    HeroSlide.objects.filter(is_active=True),
        'site_settings':  SiteSetting.get(),
        'hero_news':      News.objects.filter(is_published=True)[:3],
        'latest_news':    News.objects.filter(is_published=True)[:4],
        'announcements':  Announcement.objects.filter(is_published=True)[:6],
        'gallery_images': GalleryImage.objects.all()[:8],
        'stories':        Story.objects.all()[:3],
    }
    return render(request, 'main/home.html', context)


def news_list(request):
    news = News.objects.filter(is_published=True)
    return render(request, 'main/news_list.html', {'news': news})


def news_detail(request, pk):
    item = get_object_or_404(News, pk=pk, is_published=True)
    return render(request, 'main/news_detail.html', {
        'item':          item,
        'latest_news':   News.objects.filter(is_published=True).exclude(pk=pk)[:4],
        'announcements': Announcement.objects.filter(is_published=True)[:4],
    })


def gallery(request):
    images = GalleryImage.objects.all()
    categories = images.values_list('category', flat=True).distinct()
    return render(request, 'main/gallery.html', {'images': images, 'categories': categories})


def stories(request):
    all_stories = Story.objects.all()
    return render(request, 'main/stories.html', {'stories': all_stories})


def team(request):
    members = TeamMember.objects.all()
    categories = members.values_list('category', flat=True).distinct()
    return render(request, 'main/team.html', {'members': members, 'categories': categories})


def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for your message. We will get back to you soon.')
        return redirect('main:contact')
    return render(request, 'main/contact.html', {})


def page_view(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'main/page.html', {'page': page})
