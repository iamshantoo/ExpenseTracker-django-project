from django import forms
from django.contrib.auth.models import User
from .models import ExpenseInfo


class expenseInfo(forms.ModelForm):
    class Meta:
        model = ExpenseInfo
        fields = ('expense_name', 'cost', 'date_added')


class editExpenseInfo(forms.ModelForm):
    class Meta:
        model = ExpenseInfo
        fields = ('expense_name', 'cost')
