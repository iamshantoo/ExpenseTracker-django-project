from django import forms
from .models import ExpenseInfo, Users


class registrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = "__all__"


class loginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'password')


class expenseInfo(forms.ModelForm):
    class Meta:
        model = ExpenseInfo
        fields = "__all__"

