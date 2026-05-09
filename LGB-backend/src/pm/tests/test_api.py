"""
pm/tests/test_api.py

API integration tests for PM endpoints.
Tests use DRF's APIClient with forced authentication.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from pm.models import Phase, Project, Tag, Task

User = get_user_model()


class PMApiTestMixin:
    """Shared setup for PM API tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            name="Test Project",
            slug="test-project",
            created_by=self.user,
        )
        self.phase = Phase.objects.create(
            project=self.project,
            phase_number=1,
            name="Phase 1",
        )


class ProjectApiTests(PMApiTestMixin, TestCase):
    def test_list_projects(self):
        response = self.client.get("/api/v1/pm/projects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project(self):
        response = self.client.get(
            f"/api/v1/pm/projects/{self.project.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Project")

    def test_create_project(self):
        response = self.client.post(
            "/api/v1/pm/projects/",
            {
                "name": "New Project",
                "slug": "new-project",
                "status": "planning",
                "priority": "high",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_project_dashboard(self):
        response = self.client.get(
            f"/api/v1/pm/projects/{self.project.slug}/dashboard/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("overall_progress", response.data)
        self.assertIn("status_breakdown", response.data)

    def test_unauthenticated_rejected(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/v1/pm/projects/")
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class TaskApiTests(PMApiTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            project=self.project,
            phase=self.phase,
            task_code="API-001",
            title="Test Task",
            status="in_progress",
        )

    def test_list_tasks(self):
        response = self.client.get("/api/v1/pm/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_project(self):
        response = self.client.get(
            f"/api/v1/pm/tasks/?project={self.project.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_status(self):
        response = self.client.get(
            "/api/v1/pm/tasks/?status=in_progress"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_board(self):
        response = self.client.get("/api/v1/pm/tasks/board/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("in_progress", response.data)

    def test_complete_task(self):
        response = self.client.post(
            f"/api/v1/pm/tasks/{self.task.id}/complete/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "completed")
        self.assertIsNotNone(self.task.completed_at)

    def test_search_tasks(self):
        response = self.client.get(
            "/api/v1/pm/tasks/?search=Test"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TagApiTests(PMApiTestMixin, TestCase):
    def test_create_tag(self):
        response = self.client.post(
            "/api/v1/pm/tags/",
            {"name": "websocket", "color": "#10b981"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_tags(self):
        Tag.objects.create(name="auth")
        Tag.objects.create(name="ai")
        response = self.client.get("/api/v1/pm/tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class PhaseApiTests(PMApiTestMixin, TestCase):
    def test_list_phases(self):
        response = self.client.get("/api/v1/pm/phases/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_phase(self):
        response = self.client.get(
            f"/api/v1/pm/phases/{self.phase.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("progress_percentage", response.data)
