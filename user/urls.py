from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

from django.contrib.auth import views as auth_views


app_name='user'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html', success_url=reverse_lazy('blogs:all')), name='password_change'),
    

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user_blogs/', views.UserBlogsView.as_view(), name='user_blogs'),
    path('contact/', TemplateView.as_view(template_name = 'user/contact.html'), name='contact'),
    path('send_email/', views.sendEmail, name="send_email"),
]   