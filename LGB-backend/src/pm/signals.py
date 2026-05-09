"""
pm/signals.py

Django signals for the PM module.
Handles automated side-effects on model changes.
"""

import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import SubTask, Task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=SubTask)
def check_task_completion_on_subtask_save(sender, instance, **kwargs):
    """
    When all subtasks of a task are completed,
    automatically transition the parent task to 'review'.
    """
    task = instance.task

    if task.status in ("completed", "cancelled"):
        return

    total = task.subtasks.count()
    completed = task.subtasks.filter(status="completed").count()

    if total > 0 and total == completed and task.status != "review":
        task.status = "review"
        task.save(update_fields=["status", "updated_at"])
        logger.info(
            "Task %s auto-moved to 'review' — all %d subtasks completed.",
            task.task_code,
            total,
        )


@receiver(pre_save, sender=Task)
def set_completed_timestamp(sender, instance, **kwargs):
    """
    Auto-set completed_at when task status changes to 'completed'.
    """
    if instance.pk:
        try:
            old = Task.objects.get(pk=instance.pk)
        except Task.DoesNotExist:
            return

        if old.status != "completed" and instance.status == "completed":
            if not instance.completed_at:
                from django.utils import timezone
                instance.completed_at = timezone.now()
                logger.info(
                    "Task %s marked completed at %s.",
                    instance.task_code,
                    instance.completed_at,
                )
