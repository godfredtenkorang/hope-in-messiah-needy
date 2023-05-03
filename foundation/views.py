from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from . import forms
from django.conf import settings
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    posts = HomeBlog.objects.order_by("-date_posted")
    events = HomeEvent.objects.order_by("-start_date")
    galleries = Gallery.objects.all()
    context = {
        'posts': posts,
        'events': events,
        'galleries': galleries
    }
    return render(request, 'foundation/home.html', context)

def about(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'foundation/about.html', context)

def latest_cause(request):
    causes = LatestCause.objects.all()
    context = {
        'causes': causes,
        'title': 'Latest Causes'
    }
    return render(request, 'foundation/latest_cause.html', context)

def social_event(request):
    social_events = Event.objects.order_by('-start_date')
    context = {
        'social_events': social_events,
        'title': 'Social Events'
    }
    return render(request, 'foundation/social_event.html', context)

def blog(request):
    blogs = Blog.objects.order_by("-date_posted")
    context = {
        'blogs': blogs,
        'title': 'Blogs'
    }
    return render(request, 'foundation/blog.html', context)

class PostListView(ListView):
    model = Blog
    template_name = 'foundation/blog.html'
    context_object_name = 'blogs'
    ordering = ['-date_posted']
    paginate_by = 5
    
class PostDetailView(DetailView):
    model = Blog
    
    form = forms.CommentForm
    
    def post(self, request, *args, **kwargs):
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.post = post
            form.save()
            
            return redirect(reverse("blog-detail", kwargs={
                'pk': post.pk
            }))
    
    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post=self.object.id).count()
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count
        })
        return context
    
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, "Your form has been submitted")
        return render(request, 'foundation/contact.html')
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'foundation/contact.html', context)

def gallery(request):
    galleries = Gallery.objects.order_by('-date')
    context = {
        'galleries': galleries,
        'title': 'Gallery'
    }
    return render(request, 'foundation/gallery.html', context)

def donate(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'foundation/make_payment.html', {'payment':payment, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = forms.PaymentForm()
    context = {
        'title': 'Donate',
        'payment_form':payment_form
    }
    return render(request, 'foundation/donate.html', context)

def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('donate')