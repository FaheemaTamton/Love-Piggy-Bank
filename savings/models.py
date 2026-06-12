from django.db import models
from django.contrib.auth.models import User

class Savings(models.Model):
    REASON_CHOICES = [
        ('bonding', 'Bonding'),
        ('quarrel', 'Quarrel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} for {self.reason} on {self.date}"
