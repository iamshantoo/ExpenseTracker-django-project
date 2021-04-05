from django.urls import path
from . import views

app_name = 'ExpenseApp'


urlpatterns = [
    path('', views.HomePage, name='home_page'),
    path('expenses/', views.addExpenseInfoPage, name='expense_info'),
    path('expenses/info/', views.showExpenseInfoPage, name='show_expense_info'),
]
