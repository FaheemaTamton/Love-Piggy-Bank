from django.db import models
from django.contrib.auth.models import User

# ----- WEEKEND BONDING -----
class Bonding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekend_date = models.DateField()  # stores the date of the weekend
    done = models.BooleanField(default=False)  # True if bonding was done
