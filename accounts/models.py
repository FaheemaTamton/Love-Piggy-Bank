from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    miss_name = models.CharField(max_length=100,null=True, blank=True)
    mister_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    qr_code = models.ImageField(upload_to='qr_codes/')
    penalty_amount = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.miss_name} & {self.mister_name} Profile"

        def has_bonded_this_weekend(self):
          if not self.last_bonding_date:
            return False
        # Optional: check if last bonding date is this weekend
        today = timezone.now().date()
        return self.last_bonding_date >= today - timezone.timedelta(days=today.weekday()+2) 