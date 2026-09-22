from django.conf import settings
from django.db import models


class details(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(default='regular', max_length=10)

    def __str__(self):
        return f'{self.user.username} ({self.role})'
