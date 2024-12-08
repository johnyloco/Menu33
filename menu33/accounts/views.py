from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from menu33.accounts.forms import AppUserCreationForm, ProfileEditForm
from menu33.accounts.models import Profile

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


def profile_delete(request, pk: int):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':  # Handle deletion only on POST requests
        profile.delete()
        return redirect('home-page')  # Redirect to home after deletion
    return render(request, 'accounts/profile-delete-page.html', {'profile': profile})


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract the email username (before @)
        email = self.get_object().user.email
        context['email_username'] = email.split('@')[0]
        return context


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={'pk': self.object.pk}
        )


def homepage_logged_in(request):
    return render(request, 'common/home.html')
