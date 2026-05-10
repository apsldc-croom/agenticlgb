"""
pm/signals.py

Django signals for the PM module.
Handles automated side-effects on model changes.

Signals registered:
  - SubTask post_save  → auto-move parent Task to 'review' when all done
  - Task pre_save      → set completed_at timestamp
  - Task post_save     → write TaskStatusHistory entry on status change
"""

import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import SubTask, Task, TaskStatusHistory

logger = logging.getLogger(__name__)


# =========================================================
# SUBTASK → PARENT TASK AUTO-REVIEW
# =========================================================

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


# =========================================================
# TASK PRE-SAVE — snapshot old status for history
# =========================================================

@receiver(pre_save, sender=Task)
def capture_task_status_snapshot(sender, instance, **kwargs):
    """
    Before saving a Task, snapshot the old status into instance._old_status.
    Used by task_status_history_on_save to detect changes.
    Also auto-sets completed_at when transitioning to 'completed'.
    """
    instance._old_status = None   # default: new object

    if instance.pk:
        try:
            old = Task.objects.get(pk=instance.pk)
            instance._old_status = old.status

            # Auto-set completed_at timestamp
            if old.status != "completed" and instance.status == "completed":
                if not instance.completed_at:
                    from django.utils import timezone
                    instance.completed_at = timezone.now()
                    logger.info(
                        "Task %s marked completed at %s.",
                        instance.task_code,
                        instance.completed_at,
                    )

        except Task.DoesNotExist:
            pass


# =========================================================
# TASK POST-SAVE — write status history
# =========================================================

@receiver(post_save, sender=Task)
def task_status_history_on_save(sender, instance, created, **kwargs):
    """
    After saving a Task:
    - If created: log the initial status
    - If updated and status changed: log the transition

    The changed_by user is taken from instance._changed_by if set
    by the view/service before calling save(). Otherwise null.

    Usage in a view:
        task._changed_by = request.user
        task.save()
    """
    old_status = getattr(instance, "_old_status", None)
    changed_by = getattr(instance, "_changed_by", None)

    if created:
        # Log the initial status on task creation
        TaskStatusHistory.objects.create(
            task=instance,
            from_status="",
            to_status=instance.status,
            changed_by=changed_by,
            note="Task created.",
        )
        logger.debug(
            "Task %s created with status '%s'.",
            instance.task_code,
            instance.status,
        )

    elif old_status is not None and old_status != instance.status:
        # Log the status transition
        TaskStatusHistory.objects.create(
            task=instance,
            from_status=old_status,
            to_status=instance.status,
            changed_by=changed_by,
            note="",
        )
        logger.info(
            "Task %s status: '%s' → '%s' (by %s).",
            instance.task_code,
            old_status,
            instance.status,
            changed_by or "system",
        )

