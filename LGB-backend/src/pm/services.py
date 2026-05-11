"""
pm/services.py

Business logic layer for the PM module.
-----------------------------------------
Keeps views thin by encapsulating domain operations here.
"""

from __future__ import annotations

import logging

from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


class ProjectService:
    """Domain operations for projects."""

    @staticmethod
    @transaction.atomic
    def create_project_with_phases(project_data: dict, phases_data: list) -> "Project":
        """
        Create a project along with its initial phases in a single transaction.

        Args:
            project_data: dict of Project field values.
            phases_data: list of dicts, each containing Phase field values.

        Returns:
            Created Project instance.
        """
        from .models import Phase, Project

        project = Project.objects.create(**project_data)

        for idx, phase_data in enumerate(phases_data, start=1):
            phase_data.setdefault("phase_number", idx)
            Phase.objects.create(project=project, **phase_data)

        logger.info(
            "Created project '%s' with %d phases.",
            project.name,
            len(phases_data),
        )
        return project

    @staticmethod
    def recalculate_progress(project_id: int) -> float:
        """
        Recalculate and return the project's overall progress.
        """
        from .models import Project

        project = Project.objects.get(pk=project_id)
        return project.progress_percentage


class TaskService:
    """Domain operations for tasks."""

    @staticmethod
    @transaction.atomic
    def complete_task(task_id: int) -> "Task":
        """
        Mark a task as completed with timestamp.
        Also completes all pending subtasks.
        """
        from .models import Task

        task = Task.objects.select_for_update().get(pk=task_id)
        task.status = "completed"
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])

        # Complete any remaining subtasks
        updated = task.subtasks.exclude(
            status="completed"
        ).update(status="completed")

        logger.info(
            "Completed task %s (+ %d subtasks).",
            task.task_code,
            updated,
        )
        return task

    @staticmethod
    def get_blocked_tasks(project_id: int) -> list:
        """
        Find tasks whose dependencies are not yet completed.
        """
        from .models import Task, TaskDependency

        blocked_ids = (
            TaskDependency.objects.filter(
                task__project_id=project_id,
            )
            .exclude(depends_on__status="completed")
            .values_list("task_id", flat=True)
            .distinct()
        )

        return list(
            Task.objects.filter(pk__in=blocked_ids)
            .values("task_code", "title", "status")
        )

    @staticmethod
    def generate_task_code(project_slug: str, sequence: int) -> str:
        """
        Generate a standardised task code.
        Example: LGB-042
        """
        prefix = project_slug[:3].upper()
        return f"{prefix}-{sequence:03d}"


class PhaseService:
    """Domain operations for phases."""

    @staticmethod
    def get_current_phase(project_id: int):
        """
        Return the first non-completed phase for a project.
        """
        from .models import Phase

        return (
            Phase.objects.filter(project_id=project_id)
            .exclude(status="completed")
            .order_by("phase_number")
            .first()
        )

    @staticmethod
    def advance_phase(phase_id: int) -> "Phase":
        """
        Transition a phase to the next logical status.
        planning -> in_progress -> review -> completed
        """
        from .models import Phase

        phase = Phase.objects.get(pk=phase_id)

        transitions = {
            "planning": "in_progress",
            "in_progress": "review",
            "review": "completed",
        }

        next_status = transitions.get(phase.status)
        if next_status:
            phase.status = next_status
            phase.save(update_fields=["status"])
            logger.info(
                "Phase %s advanced to '%s'.",
                phase,
                next_status,
            )

        return phase
