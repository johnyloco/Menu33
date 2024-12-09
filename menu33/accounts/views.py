from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from menu33.accounts.forms import AppUserCreationForm, ProfileEditForm
from menu33.accounts.models import Profile
from .mixins import CustomPermissionMixin
from .tests import is_profile_owner

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)
        
        return response


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('login-page')  # Redirect to home after successful deletion

    def test_func(self):
        # Use the reusable function for permission check
        return is_profile_owner(self)

    def delete(self, request, *args, **kwargs):
        # Fetch the profile object to delete the user
        profile = self.get_object()
        user = profile.user  # Associated user

        # Delete the user and log out
        user.delete()
        logout(request)

        # Redirect to the success URL
        return redirect(self.success_url)


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    reverse_lazy = 'login-page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        # Redirect to the profile details page after a successful edit
        return reverse_lazy(
            'profile-details',
            kwargs={'pk': self.object.pk})

    def test_func(self):
        # Use the reusable function for permission check
        return is_profile_owner(self)


def homepage_logged_in(request):
    return render(request, 'common/home.html')