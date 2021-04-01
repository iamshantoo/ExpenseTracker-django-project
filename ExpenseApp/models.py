from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'User Info'

class ExpenseInfo(models.Model):
    expense_name = models.CharField(max_length=20)
    cost = models.FloatField()
    date_added = models.DateField()
    # user_expense = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Expense Info'
