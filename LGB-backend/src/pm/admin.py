"""
pm/admin.py

Django Admin configuration for all PM models.
Provides rich admin UI with search, filtering, inline editing,
and read-only computed fields.
"""

from django.contrib import admin

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
    TechDebt,
)


# ---------------------------------------------------------
# INLINES
# ---------------------------------------------------------

class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    fields = ("title", "priority", "status", "target_metric", "due_date")


class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 0
    fields = ("phase_number", "name", "status", "start_date", "end_date", "duration_weeks")


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0
    fields = ("title", "status", "target_date")


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0
    fields = ("title", "status", "sort_order")


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 0
    fields = ("name", "category", "priority", "status")


class TaskDependencyInline(admin.TabularInline):
    model = TaskDependency
    fk_name = "task"
    extra = 0
    fields = ("depends_on",)


# ---------------------------------------------------------
# MODEL ADMINS
# ---------------------------------------------------------

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name", "slug", "status", "priority",
        "progress_percentage", "created_at",
    )
    list_filter = ("status", "priority")
    search_fields = ("name", "slug", "tagline")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("progress_percentage", "created_at", "updated_at")
    inlines = [GoalInline, PhaseInline]

    fieldsets = (
        (None, {
            "fields": ("name", "slug", "tagline", "vision", "description"),
        }),
        ("Status", {
            "fields": ("status", "priority", "start_date", "target_end_date"),
        }),
        ("Links", {
            "fields": ("repo_url", "documentation_url"),
            "classes": ("collapse",),
        }),
        ("Technical", {
            "fields": ("tech_stack", "metadata"),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("created_by", "created_at", "updated_at", "progress_percentage"),
        }),
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "priority", "status", "due_date")
    list_filter = ("status", "priority", "project")
    search_fields = ("title",)


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = (
        "phase_number", "name", "project", "status",
        "start_date", "end_date", "progress_percentage",
    )
    list_filter = ("status", "project")
    search_fields = ("name",)
    readonly_fields = ("progress_percentage",)
    inlines = [MilestoneInline, FeatureInline]


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("title", "phase", "status", "target_date")
    list_filter = ("status",)
    search_fields = ("title",)


@admin.register(ArchitectureLayer)
class ArchitectureLayerAdmin(admin.ModelAdmin):
    list_display = ("layer_number", "name", "project", "status", "owner")
    list_filter = ("status", "project")
    search_fields = ("name", "owner")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "phase", "category", "priority", "status")
    list_filter = ("category", "priority", "status", "project")
    search_fields = ("name", "description")
    filter_horizontal = ("tags",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_code", "title", "project", "phase",
        "category", "priority", "status",
        "assigned_to", "due_date", "subtask_progress",
    )
    list_filter = ("status", "priority", "category", "project", "phase", "ai_generated")
    search_fields = ("task_code", "title", "description")
    readonly_fields = ("subtask_progress", "created_at", "updated_at")
    filter_horizontal = ("tags",)
    inlines = [SubTaskInline, TaskDependencyInline]

    fieldsets = (
        (None, {
            "fields": (
                "task_code", "title", "description",
                "project", "phase", "milestone", "feature",
            ),
        }),
        ("Classification", {
            "fields": ("category", "priority", "status", "tags"),
        }),
        ("Assignment", {
            "fields": ("assigned_to", "target_file"),
        }),
        ("Effort", {
            "fields": ("estimated_hours", "actual_hours", "due_date", "completed_at"),
        }),
        ("AI", {
            "fields": ("ai_generated", "ai_summary", "ai_risk_score"),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("sort_order", "subtask_progress", "created_at", "updated_at"),
        }),
    )


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "sort_order")
    list_filter = ("status",)
    search_fields = ("title",)


@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ("task", "depends_on")
    search_fields = ("task__task_code", "depends_on__task_code")


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "doc_type", "status", "completeness", "last_reviewed")
    list_filter = ("status", "doc_type", "project")
    search_fields = ("title", "file_path")


@admin.register(TechDebt)
class TechDebtAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "severity", "status", "estimated_hours", "created_at")
    list_filter = ("severity", "status", "project")
    search_fields = ("title", "description")


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ("project", "environment", "status", "version", "deployed_by", "last_deployed")
    list_filter = ("environment", "status", "project")
    search_fields = ("version", "deployed_by")


@admin.register(AIMemory)
class AIMemoryAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "memory_type", "created_at")
    list_filter = ("memory_type", "project")
    search_fields = ("title", "content")


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "insight_type", "severity", "resolved", "created_at")
    list_filter = ("insight_type", "severity", "resolved", "project")
    search_fields = ("title", "description")
