from django.urls import path
from .views import PostListView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('latest_cause/', views.latest_cause, name='latest_cause'),
    path('social_event/', views.social_event, name='social_event'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('make_payment/<str:ref>/', views.verify_payment, name='verify-payment')
]