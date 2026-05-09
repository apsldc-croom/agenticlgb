"""
pm/tests/test_signals.py

Tests for PM signal handlers.
"""

from django.test import TestCase

from pm.models import Phase, Project, SubTask, Task


class SubTaskCompletionSignalTests(TestCase):
    """Test that completing all subtasks triggers task review."""

    def setUp(self):
        self.project = Project.objects.create(
            name="P", slug="p",
        )
        self.phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Ph1",
        )
        self.task = Task.objects.create(
            project=self.project,
            phase=self.phase,
            task_code="SIG-001",
            title="Signal test",
            status="in_progress",
        )

    def test_all_subtasks_completed_moves_task_to_review(self):
        sub1 = SubTask.objects.create(
            task=self.task,
            title="Sub 1",
            status="completed",
        )
        sub2 = SubTask.objects.create(
            task=self.task,
            title="Sub 2",
            status="in_progress",
        )

        # Complete the second subtask
        sub2.status = "completed"
        sub2.save()

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "review")

    def test_partial_completion_does_not_trigger(self):
        SubTask.objects.create(
            task=self.task,
            title="Sub 1",
            status="in_progress",
        )
        sub2 = SubTask.objects.create(
            task=self.task,
            title="Sub 2",
            status="in_progress",
        )

        # Complete only one of two subtasks
        sub2.status = "completed"
        sub2.save()

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "in_progress")


class TaskCompletionTimestampSignalTests(TestCase):
    """Test that completing a task auto-sets completed_at."""

    def setUp(self):
        self.project = Project.objects.create(
            name="P", slug="p",
        )
        self.phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Ph1",
        )

    def test_completed_at_set_on_status_change(self):
        task = Task.objects.create(
            project=self.project,
            phase=self.phase,
            task_code="SIG-002",
            title="Timestamp test",
            status="in_progress",
        )
        self.assertIsNone(task.completed_at)

        task.status = "completed"
        task.save()
        task.refresh_from_db()

        self.assertIsNotNone(task.completed_at)
