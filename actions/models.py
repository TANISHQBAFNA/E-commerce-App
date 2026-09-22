from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    target = GenericForeignKey('target_ct', 'target_id')

    def __str__(self):
        return f'{self.user} {self.verb}'


def create_action(user, verb, target=None):
    action = Action(user=user, verb=verb)
    if target is not None:
        action.target = target
    action.save()
    return action
