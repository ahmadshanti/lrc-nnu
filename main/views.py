from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .models import Announcement, Event, GalleryImage, HeroSlide, News, Page, SiteSetting, Story, TeamMember


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
        name    = request.POST.get('name', '')
        email   = request.POST.get('email', '')
        subject = request.POST.get('subject', 'LRC Contact Form')
        message = request.POST.get('message', '')
        try:
            send_mail(
                subject=f'[LRC] {subject}',
                message=f'From: {name} <{email}>\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'تم إرسال رسالتك بنجاح. سنتواصل معك قريباً.')
        except Exception:
            messages.error(request, 'حدث خطأ أثناء الإرسال. يرجى المحاولة مرة أخرى.')
        return redirect('main:contact')
    return render(request, 'main/contact.html', {})


def events(request):
    all_events = Event.objects.filter(is_published=True)
    return render(request, 'main/events.html', {'events': all_events})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, 'main/event_detail.html', {'event': event})


def page_view(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'main/page.html', {'page': page})
