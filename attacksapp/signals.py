from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from attacksapp.models import Attack, STATUS_CHOICES


@receiver(pre_save, sender=Attack)
def attack_pre_save(sender, instance, **kwargs):
    try:
        old_instance = Attack.objects.get(pk=instance.pk)

        if old_instance.status == instance.status:
            return

        if instance.status == STATUS_CHOICES.RUNNING:
            instance.started_at = timezone.now()

    except Attack.DoesNotExist:
        pass
