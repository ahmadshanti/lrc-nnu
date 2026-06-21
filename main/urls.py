from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('stories/', views.stories, name='stories'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('pages/<slug:slug>/', views.page_view, name='page'),
]
