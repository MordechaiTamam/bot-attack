from django.db import models


class STATUS_CHOICES(models.TextChoices):
    NEW = 'new'
    RUNNING = 'running'
    DONE = 'done'
    STOPPED = 'stopped'


class Attack(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    name = models.CharField(max_length=256, unique=True)
    command = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.NEW)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'name: {self.name}, command: {self.command}, status: {self.status}, started_at: {self.started_at}'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'command': self.command,
            'status': self.status,
            'started_at': self.started_at,
        }

