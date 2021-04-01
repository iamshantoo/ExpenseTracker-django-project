from django.urls import path
from . import views

urlpatterns = [
    path('', views.showHomePage),
    path('signin/', views.showLoginPage, name="signin"),
    path('signup/', views.showRegistrationPage, name='signup'),
    path('expenses/', views.showExpenseInfoPage, name='expenseInfo'),
]