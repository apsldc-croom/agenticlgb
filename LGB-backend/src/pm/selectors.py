"""
pm/selectors.py

Read / query logic for the PM module.
---------------------------------------
Encapsulates complex queries, aggregations, and reporting
to keep views and services clean.
"""

from django.db.models import Count, Sum

from .models import (
    AIInsight,
    Deployment,
    Feature,
    Phase,
    Project,
    Task,
    TechDebt,
)


def get_project_summary(project_id: int) -> dict:
    """
    Comprehensive project summary for dashboard.
    """
    project = Project.objects.get(pk=project_id)

    task_stats = (
        Task.objects.filter(project_id=project_id)
        .values("status")
        .annotate(count=Count("id"))
    )

    status_map = {item["status"]: item["count"] for item in task_stats}

    return {
        "project_id": project.id,
        "name": project.name,
        "status": project.status,
        "progress": project.progress_percentage,
        "task_breakdown": status_map,
        "total_phases": project.phases.count(),
        "total_features": project.features.count(),
        "open_debt": TechDebt.objects.filter(
            project_id=project_id
        ).exclude(status="completed").count(),
        "unresolved_insights": AIInsight.objects.filter(
            project_id=project_id, resolved=False,
        ).count(),
    }


def get_tasks_by_phase(project_id: int) -> list:
    """
    Tasks grouped by phase for a given project.
    """
    phases = Phase.objects.filter(
        project_id=project_id,
    ).order_by("phase_number")

    result = []
    for phase in phases:
        tasks = (
            Task.objects.filter(phase=phase)
            .values(
                "task_code", "title", "status",
                "priority", "category",
            )
            .order_by("sort_order")
        )
        result.append({
            "phase_number": phase.phase_number,
            "phase_name": phase.name,
            "phase_status": phase.status,
            "progress": phase.progress_percentage,
            "tasks": list(tasks),
        })

    return result


def get_overdue_tasks(project_id: int = None) -> list:
    """
    Return all tasks past their due date that aren't completed.
    """
    from django.utils import timezone

    qs = Task.objects.filter(
        due_date__lt=timezone.now().date(),
    ).exclude(
        status__in=["completed", "cancelled"],
    )

    if project_id:
        qs = qs.filter(project_id=project_id)

    return list(
        qs.values(
            "task_code", "title", "status",
            "priority", "due_date",
            "project__name",
        ).order_by("due_date")
    )


def get_effort_summary(project_id: int) -> dict:
    """
    Estimated vs. actual hours for a project.
    """
    agg = Task.objects.filter(
        project_id=project_id,
    ).aggregate(
        total_estimated=Sum("estimated_hours"),
        total_actual=Sum("actual_hours"),
    )

    return {
        "estimated_hours": agg["total_estimated"] or 0,
        "actual_hours": agg["total_actual"] or 0,
        "variance": (agg["total_actual"] or 0) - (agg["total_estimated"] or 0),
    }


def get_feature_coverage(project_id: int) -> dict:
    """
    Feature breakdown by category and status.
    """
    features = (
        Feature.objects.filter(project_id=project_id)
        .values("category", "status")
        .annotate(count=Count("id"))
    )

    return list(features)


def get_deployment_status(project_id: int) -> list:
    """
    Current deployment status across all environments.
    """
    return list(
        Deployment.objects.filter(project_id=project_id)
        .values(
            "environment", "status", "version",
            "url", "last_deployed",
        )
        .order_by("environment")
    )
