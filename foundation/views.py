from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from . import forms
from django.conf import settings
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'foundation/home.html')

def about(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'foundation/about.html', context)

def latest_cause(request):
    context = {
        'title': 'Latest Causes'
    }
    return render(request, 'foundation/latest_cause.html', context)

def social_event(request):
    context = {
        'title': 'Social Events'
    }
    return render(request, 'foundation/social_event.html', context)

def blog(request):
    context = {
        'title': 'Blogs'
    }
    return render(request, 'foundation/blog.html', context)

def contact(request):
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'foundation/contact.html', context)

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
        return redirect('home')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('donate')