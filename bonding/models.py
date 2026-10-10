from django.db import models
from django.contrib.auth.models import User

# ----- WEEKEND BONDING -----
class Bonding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekend_date = models.DateField()  # stores the date of the weekend
    done = models.BooleanField(default=False)  # True if bonding was done

    def __str__(self):
        status = "Done" if self.done else "Skipped"
        return f"{self.user.username} - {self.weekend_date} ({status})"


# ----- QUARREL LOG -----
class Quarrel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # logs when quarrel happened
    reason = models.CharField(max_length=200, blank=True, null=True)  # optional

    def __str__(self):
                return f"{self.user.username} - {self.date} ({self.reason})"
