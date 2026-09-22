from django.conf import settings
from django.db import models


class newitem(models.Model):
    title = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    type = models.CharField(max_length=50, blank=True, default='')
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')
    cart_items = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(newitem, on_delete=models.CASCADE)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} on {self.item}'
