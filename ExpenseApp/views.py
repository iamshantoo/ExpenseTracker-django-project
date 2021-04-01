from django.shortcuts import render
# from django.http import HttpResponse
from .forms import registrationForm, loginForm, expenseInfo

def showHomePage(request):
    return render(request, "Home/homepage.html")

def showLoginPage(request):
    form = loginForm()
    return render(request, "Home/login.html", {'form':form})

def showRegistrationPage(request):
    form = registrationForm()
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "Home/register.html", {'form': form})

def showExpenseInfoPage(request):
    form = expenseInfo()
    if request.method == 'POST':
        form = expenseInfo(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "Home/expenses.html", {'form': form})
