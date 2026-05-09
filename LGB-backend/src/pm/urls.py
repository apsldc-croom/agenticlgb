"""
pm/urls.py

URL routing for the PM API.
All endpoints are registered via DRF's DefaultRouter.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "pm"

router = DefaultRouter()

router.register(r"tags", views.TagViewSet, basename="tag")
router.register(r"projects", views.ProjectViewSet, basename="project")
router.register(r"goals", views.GoalViewSet, basename="goal")
router.register(r"phases", views.PhaseViewSet, basename="phase")
router.register(r"milestones", views.MilestoneViewSet, basename="milestone")
router.register(r"architecture-layers", views.ArchitectureLayerViewSet, basename="architecture-layer")
router.register(r"features", views.FeatureViewSet, basename="feature")
router.register(r"tasks", views.TaskViewSet, basename="task")
router.register(r"subtasks", views.SubTaskViewSet, basename="subtask")
router.register(r"task-dependencies", views.TaskDependencyViewSet, basename="task-dependency")
router.register(r"docs", views.DocumentationViewSet, basename="documentation")
router.register(r"tech-debt", views.TechDebtViewSet, basename="tech-debt")
router.register(r"deployments", views.DeploymentViewSet, basename="deployment")
router.register(r"ai-memories", views.AIMemoryViewSet, basename="ai-memory")
router.register(r"ai-insights", views.AIInsightViewSet, basename="ai-insight")

urlpatterns = [
    path("", include(router.urls)),
]
