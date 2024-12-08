from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
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
    success_url = reverse_lazy('home-page')  # Redirect to home after successful deletion

    def test_func(self):
        # Use the reusable function for permission check
        return is_profile_owner(self)


class ProfileDetailsView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract the email username (before @)
        email = self.get_object().user.email
        context['email_username'] = email.split('@')[0]
        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        # Allow the user to edit only their profile
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        # Redirect to the profile details page after a successful edit
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        # Use the reusable function for permission check
        return is_profile_owner(self)


def homepage_logged_in(request):
    return render(request, 'common/home.html')