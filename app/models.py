from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name='event_created'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    name = models.CharField(
        max_length=255,
        blank=True
    )
    participants = models.ManyToManyField(
        get_user_model(),
        related_name='event_participated'
    )

    def is_participant(self, user_id):
        return self.participants.filter(id=user_id).exists()


class Gift(models.Model):
    added_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    added_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contributors = models.ManyToManyField(
        get_user_model(),
        related_name='contributors'
    )
    # url = models

    def is_contributor(self, user_id):
        return self.contributors.filter(id=user_id).exists()