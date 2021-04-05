from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ExpenseInfo(models.Model):
    user = models.ForeignKey(
        User, related_name='user_expense_info', on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=20)
    cost = models.FloatField()
    date_added = models.DateField()

    class Meta:
        db_table = 'Expense Info'

    def __str__(self):
        return self.expense_name
