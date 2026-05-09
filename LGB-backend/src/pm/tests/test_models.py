"""
pm/tests/test_models.py

Unit tests for PM models — field defaults, properties, constraints.
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from pm.models import (
    ArchitectureLayer,
    Feature,
    Goal,
    Milestone,
    Phase,
    Project,
    SubTask,
    Tag,
    Task,
    TaskDependency,
)

User = get_user_model()


class TagModelTests(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="auth")
        self.assertEqual(str(tag), "auth")
        self.assertEqual(tag.color, "#6366f1")

    def test_unique_tag_name(self):
        Tag.objects.create(name="unique-tag")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="unique-tag")


class ProjectModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            slug="test-project",
            tagline="A test project",
        )

    def test_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_default_status(self):
        self.assertEqual(self.project.status, "planning")

    def test_default_priority(self):
        self.assertEqual(self.project.priority, "medium")

    def test_progress_no_tasks(self):
        self.assertEqual(self.project.progress_percentage, 0)

    def test_progress_with_tasks(self):
        phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Phase 1",
        )
        Task.objects.create(
            project=self.project,
            phase=phase,
            task_code="TST-001",
            title="Task 1",
            status="completed",
        )
        Task.objects.create(
            project=self.project,
            phase=phase,
            task_code="TST-002",
            title="Task 2",
            status="in_progress",
        )
        self.assertEqual(self.project.progress_percentage, 50.0)

    def test_unique_slug(self):
        with self.assertRaises(IntegrityError):
            Project.objects.create(
                name="Another",
                slug="test-project",
            )


class PhaseModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="P", slug="p",
        )
        self.phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Foundation",
        )

    def test_str(self):
        self.assertEqual(str(self.phase), "P1 - Foundation")

    def test_unique_phase_per_project(self):
        with self.assertRaises(IntegrityError):
            Phase.objects.create(
                project=self.project,
                phase_number=1,
                name="Duplicate",
            )

    def test_progress(self):
        self.assertEqual(self.phase.progress_percentage, 0)


class TaskModelTests(TestCase):
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
            task_code="TST-001",
            title="Implement auth",
        )

    def test_str(self):
        self.assertEqual(str(self.task), "[TST-001] Implement auth")

    def test_subtask_progress_empty(self):
        self.assertEqual(self.task.subtask_progress, "0/0")

    def test_subtask_progress_with_items(self):
        SubTask.objects.create(
            task=self.task,
            title="Sub 1",
            status="completed",
        )
        SubTask.objects.create(
            task=self.task,
            title="Sub 2",
            status="in_progress",
        )
        self.assertEqual(self.task.subtask_progress, "1/2")

    def test_unique_task_code(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(
                project=self.project,
                phase=self.phase,
                task_code="TST-001",
                title="Duplicate code",
            )


class TaskDependencyTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="P", slug="p",
        )
        self.phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Ph1",
        )
        self.task_a = Task.objects.create(
            project=self.project,
            phase=self.phase,
            task_code="A-001",
            title="Task A",
        )
        self.task_b = Task.objects.create(
            project=self.project,
            phase=self.phase,
            task_code="B-001",
            title="Task B",
        )

    def test_dependency_str(self):
        dep = TaskDependency.objects.create(
            task=self.task_b,
            depends_on=self.task_a,
        )
        self.assertEqual(
            str(dep),
            "B-001 depends on A-001",
        )

    def test_unique_dependency(self):
        TaskDependency.objects.create(
            task=self.task_b,
            depends_on=self.task_a,
        )
        with self.assertRaises(IntegrityError):
            TaskDependency.objects.create(
                task=self.task_b,
                depends_on=self.task_a,
            )


class GoalModelTests(TestCase):
    def test_str(self):
        project = Project.objects.create(
            name="P", slug="p",
        )
        goal = Goal.objects.create(
            project=project,
            title="Ship MVP",
        )
        self.assertEqual(str(goal), "Ship MVP")


class ArchitectureLayerTests(TestCase):
    def test_str(self):
        project = Project.objects.create(
            name="P", slug="p",
        )
        layer = ArchitectureLayer.objects.create(
            project=project,
            layer_number=3,
            name="API Gateway",
        )
        self.assertEqual(str(layer), "L3 - API Gateway")
