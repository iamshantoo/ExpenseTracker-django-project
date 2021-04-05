from django.urls import path
from . import views

app_name = 'AccountsApp'


urlpatterns = [
    path('register/', views.RegistrationView, name='registration_view'),
    path('login/', views.LoginView, name='login_view'),
    path('logout/', views.LogoutView, name='logout_view'),
    path('profile/', views.profile, name='profile_view'),
    path('change-profile/', views.user_change, name='user_change'),
    path('password/', views.pass_change, name='pass_change'),
    path('add-picture/', views.add_pro_pic, name='add_pro_pic'),
    path('change-picture/', views.change_pro_pic, name='change_pro_pic'),
]
