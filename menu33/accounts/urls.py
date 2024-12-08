from django.contrib.auth.views import LogoutView
from django.urls import path, include
from menu33.accounts import views


from django.urls import path
from menu33.accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('welcome/', views.homepage_logged_in, name='home'),
    path('login/', views.AppUserLoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.AppUserRegisterView.as_view(), name='register-page'),
    path('profile/<int:pk>/', views.ProfileDetailsView.as_view(), name='profile-details'),
    path('profile/<int:pk>/edit/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
]
