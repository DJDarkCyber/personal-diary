from django.urls import path
from . import views


urlpatterns = [
        path("", views.main, name='index'),
        path("SignIn", views.singIn, name="SignIn"),
        path('Register', views.registerForm, name='Register'),
        path('handleRegister', views.handleRegister, name='handleRegister'),
        path("handleLogin", views.handleLogin, name="handleLogin"),
        path("settings", views.userSettings, name='settings'),
        path("logout", views.handleLogout, name='logout'),
        path("changePassword", views.changePassword, name='changePassword'),
        path("quotes", views.publicQuotes, name='quotes'),
        path('handle_quote', views.handle_quote, name='handle_quote'),
        path("handle_names", views.handle_names, name='handle_names'),
        path('diary', views.yourDiary, name='diary'),
        path('handle_diary', views.handle_diary, name='handle_diary'),
        path('about', views.aboutMe, name='about'),
]

