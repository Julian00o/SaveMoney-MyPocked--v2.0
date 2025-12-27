# transactions/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('income', 'Доход'), ('expense', 'Расход')])
    icon = models.CharField(max_length=50, default='💰')
    color = models.CharField(max_length=20, default='#3498db')
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('income', 'Доход'), ('expense', 'Расход')])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title