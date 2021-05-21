"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path #include other routes to our other apps
from users import views as user_views # other option which makes possible to create urls in main project directory without creating urls.py in the app
from django.contrib.auth import views as auth_views

from django.conf import settings # for pages to be able to access our Media
from django.conf.urls.static import static # for pages to be able to access our Media


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name="profile"),

    path('subscription/', user_views.subscription, name="subscription"),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"), #classbased views, template_name is to tell django where to look for template
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('', include('blog.urls')),
    path('data/', include('data.urls')), # mapping to our blog.urls
    re_path('djga/', include('google_analytics.urls')),
]

if settings.DEBUG: # if currently in Debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for pages to be able to access our Media
