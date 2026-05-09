"""
pm/tests/test_services.py

Tests for the PM service layer.
"""

from django.test import TestCase

from pm.models import Phase, Project, SubTask, Task
from pm.services import PhaseService, ProjectService, TaskService


class ProjectServiceTests(TestCase):
    def test_create_project_with_phases(self):
        project = ProjectService.create_project_with_phases(
            project_data={
                "name": "LGB Platform",
                "slug": "lgb-platform",
            },
            phases_data=[
                {"name": "Foundation"},
                {"name": "Core Platform"},
                {"name": "Social Layer"},
            ],
        )
        self.assertEqual(project.phases.count(), 3)
        self.assertEqual(
            project.phases.first().phase_number, 1,
        )

    def test_recalculate_progress(self):
        project = Project.objects.create(
            name="P", slug="p",
        )
        phase = Phase.objects.create(
            project=project,
            phase_number=1,
            name="Ph1",
        )
        Task.objects.create(
            project=project,
            phase=phase,
            task_code="X-001",
            title="Done",
            status="completed",
        )
        Task.objects.create(
            project=project,
            phase=phase,
            task_code="X-002",
            title="WIP",
            status="in_progress",
        )
        progress = ProjectService.recalculate_progress(project.id)
        self.assertEqual(progress, 50.0)


class TaskServiceTests(TestCase):
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
            task_code="SVC-001",
            title="Test task",
            status="in_progress",
        )

    def test_complete_task(self):
        SubTask.objects.create(
            task=self.task,
            title="Sub 1",
            status="in_progress",
        )
        result = TaskService.complete_task(self.task.id)
        self.assertEqual(result.status, "completed")
        self.assertIsNotNone(result.completed_at)
        # Subtask should also be completed
        self.assertEqual(
            self.task.subtasks.filter(status="completed").count(),
            1,
        )

    def test_generate_task_code(self):
        code = TaskService.generate_task_code("lgb-platform", 42)
        self.assertEqual(code, "LGB-042")

    def test_get_blocked_tasks(self):
        blocker = Task.objects.create(
            project=self.project,
            phase=self.phase,
            task_code="SVC-002",
            title="Blocker",
            status="in_progress",
        )
        from pm.models import TaskDependency

        TaskDependency.objects.create(
            task=self.task,
            depends_on=blocker,
        )
        blocked = TaskService.get_blocked_tasks(self.project.id)
        codes = [t["task_code"] for t in blocked]
        self.assertIn("SVC-001", codes)


class PhaseServiceTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="P", slug="p",
        )
        self.phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Foundation",
            status="planning",
        )

    def test_get_current_phase(self):
        current = PhaseService.get_current_phase(self.project.id)
        self.assertEqual(current, self.phase)

    def test_advance_phase(self):
        result = PhaseService.advance_phase(self.phase.id)
        self.assertEqual(result.status, "in_progress")

        result = PhaseService.advance_phase(self.phase.id)
        self.assertEqual(result.status, "review")

        result = PhaseService.advance_phase(self.phase.id)
        self.assertEqual(result.status, "completed")
