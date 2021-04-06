from django.shortcuts import render
from django.urls import reverse
from .forms import expenseInfo
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ExpenseInfo

# Create your views here.


def HomePage(request):
    return render(request, "HomePage.html", {})


@login_required
def addExpenseInfoPage(request):
    form = expenseInfo()
    if request.method == 'POST':
        form = expenseInfo(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            messages.success(request, f"Information added Successfully.")
            return HttpResponseRedirect(reverse('AccountsApp:profile_view'))
    dict = {'form': form}
    return render(request, "addExpenseInfoPage.html", context=dict)


@login_required
def showExpenseInfoPage(request):
    data = ExpenseInfo.objects.filter(user=request.user)
    return render(request, 'showExpenseInfoPage.html', context={'data': data})
