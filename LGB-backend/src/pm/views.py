"""
pm/views.py

DRF ViewSets for the PM module.
---------------------------------
All ViewSets use ModelViewSet for full CRUD.
List vs. detail serializers are swapped via get_serializer_class().
Custom actions expose additional endpoints (e.g., dashboard stats).
"""

from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import FeatureFilter, TaskFilter
from .models import (
    AIInsight,
    AIMemory,
    ArchitectureLayer,
    Deployment,
    Documentation,
    Feature,
    Goal,
    Milestone,
    Phase,
    Project,
    SubTask,
    Tag,
    Task,
    TaskDependency,
    TaskStatusHistory,
    TechDebt,
)
from .serializers import (
    AIInsightSerializer,
    AIMemorySerializer,
    ArchitectureLayerSerializer,
    DeploymentSerializer,
    DocumentationSerializer,
    FeatureDetailSerializer,
    FeatureListSerializer,
    GoalSerializer,
    MilestoneSerializer,
    PhaseDetailSerializer,
    PhaseListSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    SubTaskSerializer,
    TagSerializer,
    TaskDetailSerializer,
    TaskDependencySerializer,
    TaskListSerializer,
    TaskStatusHistorySerializer,
    TechDebtSerializer,
)


# =========================================================
# TAG
# =========================================================

class TagViewSet(viewsets.ModelViewSet):
    """CRUD for tags used across features and tasks."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]


# =========================================================
# PROJECT
# =========================================================

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for projects.

    Endpoints:
      GET    /projects/              — list all projects
      POST   /projects/              — create project
      GET    /projects/{slug}/       — project detail
      PUT    /projects/{slug}/       — update project
      DELETE /projects/{slug}/       — delete project
      GET    /projects/{slug}/dashboard/ — project health dashboard
    """

    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["name", "tagline", "description"]
    ordering_fields = ["created_at", "name", "priority"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def dashboard(self, request, slug=None):
        """
        Project health dashboard with aggregated stats.
        """
        project = self.get_object()

        tasks = project.tasks.all()
        total_tasks = tasks.count()
        status_breakdown = dict(
            tasks.values_list("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )

        phases = project.phases.all()
        phase_progress = [
            {
                "phase_number": p.phase_number,
                "name": p.name,
                "status": p.status,
                "progress": p.progress_percentage,
            }
            for p in phases
        ]

        priority_breakdown = dict(
            tasks.values_list("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )
        category_breakdown = dict(
            tasks.values_list("category")
            .annotate(count=Count("id"))
            .values_list("category", "count")
        )

        return Response({
            "project": project.name,
            "overall_progress": project.progress_percentage,
            "total_tasks": total_tasks,
            "status_breakdown": status_breakdown,
            "priority_breakdown": priority_breakdown,
            "category_breakdown": category_breakdown,
            "phases": phase_progress,
            "open_tech_debt": project.tech_debts.exclude(status="completed").count(),
            "unresolved_insights": project.ai_insights.filter(resolved=False).count(),
        })


# =========================================================
# GOAL
# =========================================================

class GoalViewSet(viewsets.ModelViewSet):
    """CRUD for project goals."""

    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["project", "status", "priority"]
    ordering = ["sort_order"]

    def get_queryset(self):
        qs = Goal.objects.all()
        project = self.request.query_params.get("project")
        if project:
            qs = qs.filter(project_id=project)
        return qs


# =========================================================
# PHASE
# =========================================================

class PhaseViewSet(viewsets.ModelViewSet):
    """CRUD for project phases."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["project", "status"]
    ordering = ["phase_number"]

    def get_queryset(self):
        qs = Phase.objects.select_related("project").prefetch_related(
            "milestones", "features", "tasks",
        )
        project = self.request.query_params.get("project")
        if project:
            qs = qs.filter(project_id=project)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return PhaseListSerializer
        return PhaseDetailSerializer


# =========================================================
# MILESTONE
# =========================================================

class MilestoneViewSet(viewsets.ModelViewSet):
    """CRUD for milestones within phases."""

    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["phase", "status"]

    def get_queryset(self):
        qs = Milestone.objects.select_related("phase")
        phase = self.request.query_params.get("phase")
        if phase:
            qs = qs.filter(phase_id=phase)
        return qs


# =========================================================
# ARCHITECTURE LAYER
# =========================================================

class ArchitectureLayerViewSet(viewsets.ModelViewSet):
    """CRUD for architecture layers."""

    serializer_class = ArchitectureLayerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project", "status"]

    def get_queryset(self):
        qs = ArchitectureLayer.objects.all()
        project = self.request.query_params.get("project")
        if project:
            qs = qs.filter(project_id=project)
        return qs


# =========================================================
# FEATURE
# =========================================================

class FeatureViewSet(viewsets.ModelViewSet):
    """CRUD for product features."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FeatureFilter
    search_fields = ["name", "description"]
    ordering_fields = ["name", "priority", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        return Feature.objects.select_related(
            "project", "phase",
        ).prefetch_related("tags")

    def get_serializer_class(self):
        if self.action == "list":
            return FeatureListSerializer
        return FeatureDetailSerializer


# =========================================================
# TASK
# =========================================================

class TaskViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for tasks.

    Extra actions:
      GET /tasks/board/         — Kanban board grouped by status
      POST /tasks/{id}/complete/ — Mark task as completed
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["task_code", "title", "description"]
    ordering_fields = ["sort_order", "task_code", "priority", "due_date", "created_at"]
    ordering = ["sort_order", "task_code"]

    def get_queryset(self):
        return Task.objects.select_related(
            "project", "phase", "milestone", "feature", "assigned_to",
        ).prefetch_related("tags", "subtasks")

    def get_serializer_class(self):
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer

    @action(detail=False, methods=["get"])
    def board(self, request):
        """
        Kanban-style board: tasks grouped by status.
        Optionally filtered by ?project=<id>.
        """
        qs = self.filter_queryset(self.get_queryset())
        grouped = {}

        for status_val, status_label in Task._meta.get_field("status").choices:
            tasks_in_status = qs.filter(status=status_val)
            grouped[status_val] = {
                "label": status_label,
                "count": tasks_in_status.count(),
                "tasks": TaskListSerializer(
                    tasks_in_status[:50], many=True
                ).data,
            }

        return Response(grouped)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Mark a task as completed with timestamp."""
        from django.utils import timezone

        task = self.get_object()
        task._changed_by = request.user   # picked up by signal
        task.status = "completed"
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return Response(
            TaskDetailSerializer(task).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="bulk-update")
    def bulk_update(self, request):
        """
        POST /api/v1/pm/tasks/bulk-update/
        Body: { "ids": [1, 2, 3], "status": "in_progress" }

        Bulk-update status for multiple tasks.
        Each transition is recorded via the signal (changed_by = request.user).
        """
        ids = request.data.get("ids", [])
        new_status = request.data.get("status", "")

        valid_statuses = [c[0] for c in Task._meta.get_field("status").choices]
        if not ids or new_status not in valid_statuses:
            return Response(
                {"error": "Provide 'ids' (list) and a valid 'status'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tasks = Task.objects.filter(id__in=ids)
        updated_count = 0
        for task in tasks:
            if task.status != new_status:
                task._changed_by = request.user
                task.status = new_status
                task.save(update_fields=["status", "updated_at"])
                updated_count += 1

        return Response(
            {"updated": updated_count, "skipped": len(ids) - updated_count},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="history")
    def task_history(self, request, pk=None):
        """
        GET /api/v1/pm/tasks/{id}/history/
        Returns the status change timeline for a task.
        """
        task = self.get_object()
        history = TaskStatusHistory.objects.filter(
            task=task
        ).select_related("changed_by").order_by("-changed_at")
        return Response(
            TaskStatusHistorySerializer(history, many=True).data
        )


# =========================================================
# SUBTASK
# =========================================================

class SubTaskViewSet(viewsets.ModelViewSet):
    """CRUD for subtasks within tasks."""

    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["task", "status"]

    def get_queryset(self):
        qs = SubTask.objects.select_related("task")
        task = self.request.query_params.get("task")
        if task:
            qs = qs.filter(task_id=task)
        return qs


# =========================================================
# TASK DEPENDENCY
# =========================================================

class TaskDependencyViewSet(viewsets.ModelViewSet):
    """CRUD for task dependency edges."""

    serializer_class = TaskDependencySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskDependency.objects.select_related(
            "task", "depends_on",
        )


# =========================================================
# DOCUMENTATION
# =========================================================

class DocumentationViewSet(viewsets.ModelViewSet):
    """CRUD for documentation tracking entries."""

    serializer_class = DocumentationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["project", "status", "doc_type"]
    search_fields = ["title", "file_path"]

    def get_queryset(self):
        return Documentation.objects.select_related("project")


# =========================================================
# TECH DEBT
# =========================================================

class TechDebtViewSet(viewsets.ModelViewSet):
    """CRUD for tech debt tracking."""

    serializer_class = TechDebtSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project", "severity", "status"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return TechDebt.objects.select_related("project")


# =========================================================
# DEPLOYMENT
# =========================================================

class DeploymentViewSet(viewsets.ModelViewSet):
    """CRUD for deployment tracking."""

    serializer_class = DeploymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project", "environment", "status"]

    def get_queryset(self):
        return Deployment.objects.select_related("project")


# =========================================================
# AI MEMORY
# =========================================================

class AIMemoryViewSet(viewsets.ModelViewSet):
    """CRUD for AI long-term memory entries."""

    serializer_class = AIMemorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["project", "memory_type"]
    search_fields = ["title", "content"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return AIMemory.objects.select_related("project")


# =========================================================
# AI INSIGHT
# =========================================================

class AIInsightViewSet(viewsets.ModelViewSet):
    """CRUD for AI-generated insights."""

    serializer_class = AIInsightSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["project", "insight_type", "severity", "resolved"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return AIInsight.objects.select_related("project", "task")

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        """Mark an insight as resolved."""
        insight = self.get_object()
        insight.resolved = True
        insight.save(update_fields=["resolved"])
        return Response(
            AIInsightSerializer(insight).data,
            status=status.HTTP_200_OK,
        )
