from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, RedirectView
from rest_framework.permissions import IsAuthenticated

from blog.models import Blog
from users.forms import UserRegisterForm, UserProfileForm, SubscriptionForm
from users.models import User, Subscription
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/user_register.html"
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


def login_view(request):
    return render(request, 'users/login.html')


def register_view(request):
    return render(request, 'users/register.html')


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('users:login')
    return render(request, 'users/logout.html')


@login_required(login_url=reverse_lazy('users:login'))
def perform_create(self, request):
    if request.method == 'GET':
        if hasattr(request.user, 'subscription') and request.user.subscription:
            raise PermissionDenied
        else:
            user = User.objects.get(pk=request.user.pk)
            payment = Subscription.objects.create(payment_data=datetime.now())
            create_stripe_product(
                payment.pk, payment.payment_data
            )
            price = create_stripe_price()
            session_id, payment_url = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = payment_url
            user.payment = payment
            user.save()
            payment.save()
            return HttpResponsePermanentRedirect(payment.payment_url)
