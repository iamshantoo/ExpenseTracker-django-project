from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import expenseInfo, editExpenseInfo
# from .forms import expenseInfo
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ExpenseInfo
from .utils import get_plot
from django.db.models import Sum
import re
import json

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
            return HttpResponseRedirect(reverse('ExpenseApp:show_expense_info'))
    dict = {'form': form}
    return render(request, "addExpenseInfoPage.html", context=dict)


@login_required
def showExpenseInfoPage(request):
    count = ExpenseInfo.objects.aggregate(Sum('cost'))
    l = json.dumps(count)
    total = re.findall("\d+", l)
    data = ExpenseInfo.objects.filter(user=request.user)
    return render(request, 'showExpenseInfoPage.html', context={'data': data, 'sum': total})


@login_required
def update(request, id):
    instance = get_object_or_404(ExpenseInfo, id=id)
    form = editExpenseInfo(data=request.POST, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        "expense_name": instance.expense_name,
        "cost": instance.cost,
        "instance": instance,
        "form": form,
    }
    return render(request, 'editExpenseInfoPage.html', context=context)


@login_required
def delete(request, id):
    deleteitem = get_object_or_404(ExpenseInfo, pk=id).delete()
    return HttpResponseRedirect(reverse('ExpenseApp:show_expense_info'))


def graph_view(request):
    qs = ExpenseInfo.objects.filter(user=request.user)
    x = [x.expense_name for x in qs]
    y = [y.cost for y in qs]
    chart = get_plot(x, y)
    return render(request, 'graphView.html', {'chart': chart})
