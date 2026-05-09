"""
pm/filters.py

Django-filter FilterSets for PM models.
Provides advanced query parameter filtering for the API.
"""

from django_filters import rest_framework as django_filters

from .models import Feature, Task


class TaskFilter(django_filters.FilterSet):
    """
    Filterable query parameters for tasks:
      ?project=1
      ?phase=2
      ?status=in_progress
      ?priority=high
      ?category=backend
      ?assigned_to=3
      ?ai_generated=true
      ?due_before=2026-06-01
      ?due_after=2026-05-01
      ?search=auth
    """

    project = django_filters.NumberFilter(field_name="project_id")
    phase = django_filters.NumberFilter(field_name="phase_id")
    milestone = django_filters.NumberFilter(field_name="milestone_id")
    feature = django_filters.NumberFilter(field_name="feature_id")
    assigned_to = django_filters.NumberFilter(field_name="assigned_to_id")
    ai_generated = django_filters.BooleanFilter(field_name="ai_generated")

    due_before = django_filters.DateFilter(
        field_name="due_date",
        lookup_expr="lte",
    )
    due_after = django_filters.DateFilter(
        field_name="due_date",
        lookup_expr="gte",
    )

    class Meta:
        model = Task
        fields = [
            "project", "phase", "milestone", "feature",
            "status", "priority", "category",
            "assigned_to", "ai_generated",
        ]


class FeatureFilter(django_filters.FilterSet):
    """
    Filterable query parameters for features:
      ?project=1
      ?phase=2
      ?category=backend
      ?status=in_progress
      ?user_facing=true
    """

    project = django_filters.NumberFilter(field_name="project_id")
    phase = django_filters.NumberFilter(field_name="phase_id")
    user_facing = django_filters.BooleanFilter(field_name="user_facing")

    class Meta:
        model = Feature
        fields = [
            "project", "phase",
            "category", "priority", "status",
            "user_facing",
        ]
