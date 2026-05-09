"""
pm/models.py

AI-Native Project Management Models
-----------------------------------

Purpose:
- Project intelligence hub
- Engineering operations tracking
- AI/LLM-ready structured PM system
- Architecture-aware roadmap management

Designed for:
- Django
- PostgreSQL
- Agentic PM systems
- LLM orchestration
"""

from django.conf import settings
from django.db import models


# =========================================================
# COMMON CHOICES
# =========================================================

STATUS_CHOICES = [
    ("not_started", "Not Started"),
    ("planning", "Planning"),
    ("in_progress", "In Progress"),
    ("review", "Review"),
    ("blocked", "Blocked"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]

PRIORITY_CHOICES = [
    ("critical", "Critical"),
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low"),
]

CATEGORY_CHOICES = [
    ("backend", "Backend"),
    ("frontend", "Frontend"),
    ("ai_ml", "AI/ML"),
    ("devops", "DevOps"),
    ("infra", "Infrastructure"),
    ("security", "Security"),
    ("testing", "Testing"),
    ("docs", "Documentation"),
    ("database", "Database"),
]

ENVIRONMENT_CHOICES = [
    ("local", "Local"),
    ("dev", "Development"),
    ("staging", "Staging"),
    ("production", "Production"),
]

DOC_STATUS_CHOICES = [
    ("missing", "Missing"),
    ("draft", "Draft"),
    ("review", "Review"),
    ("published", "Published"),
    ("stale", "Stale"),
]


# =========================================================
# TAG
# =========================================================

class Tag(models.Model):
    """
    Generic categorization tags.
    Example:
    - ai
    - rag
    - auth
    - websocket
    """

    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#6366f1")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# PROJECT
# =========================================================

class Project(models.Model):
    """
    Top-level project.
    Example:
    - Elitie
    - SLDC AI Platform
    - Grid Intelligence System
    """

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    tagline = models.CharField(
        max_length=300,
        blank=True,
    )

    vision = models.TextField(blank=True)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    repo_url = models.URLField(blank=True)

    documentation_url = models.URLField(blank=True)

    tech_stack = models.JSONField(
        default=list,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_projects",
    )

    start_date = models.DateField(null=True, blank=True)

    target_end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def progress_percentage(self):
        total = self.tasks.count()

        if total == 0:
            return 0

        completed = self.tasks.filter(
            status="completed"
        ).count()

        return round((completed / total) * 100, 1)


# =========================================================
# GOAL
# =========================================================

class Goal(models.Model):
    """
    High-level strategic objective.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="goals",
    )

    title = models.CharField(max_length=300)

    description = models.TextField(blank=True)

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    target_metric = models.CharField(
        max_length=200,
        blank=True,
    )

    current_value = models.CharField(
        max_length=100,
        blank=True,
    )

    target_value = models.CharField(
        max_length=100,
        blank=True,
    )

    due_date = models.DateField(null=True, blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title


# =========================================================
# PHASE
# =========================================================

class Phase(models.Model):
    """
    Project execution phase.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="phases",
    )

    phase_number = models.PositiveIntegerField()

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    start_date = models.DateField(null=True, blank=True)

    end_date = models.DateField(null=True, blank=True)

    duration_weeks = models.PositiveIntegerField(default=2)

    architecture_layers = models.JSONField(
        default=list,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["phase_number"]

        unique_together = [
            ("project", "phase_number")
        ]

    def __str__(self):
        return f"P{self.phase_number} - {self.name}"

    @property
    def progress_percentage(self):
        total = self.tasks.count()

        if total == 0:
            return 0

        completed = self.tasks.filter(
            status="completed"
        ).count()

        return round((completed / total) * 100, 1)


# =========================================================
# MILESTONE
# =========================================================

class Milestone(models.Model):
    """
    Important delivery checkpoint.
    """

    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
        related_name="milestones",
    )

    title = models.CharField(max_length=300)

    description = models.TextField(blank=True)

    deliverable = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    target_date = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["target_date"]

    def __str__(self):
        return self.title


# =========================================================
# ARCHITECTURE LAYER
# =========================================================

class ArchitectureLayer(models.Model):
    """
    Tracks architecture modules/layers.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="architecture_layers_rel",
    )

    layer_number = models.PositiveIntegerField()

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    directory = models.CharField(
        max_length=300,
        blank=True,
    )

    owner = models.CharField(
        max_length=100,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    dependencies = models.JSONField(
        default=list,
        blank=True,
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["layer_number"]

        unique_together = [
            ("project", "layer_number")
        ]

    def __str__(self):
        return f"L{self.layer_number} - {self.name}"


# =========================================================
# FEATURE
# =========================================================

class Feature(models.Model):
    """
    Product feature lifecycle.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="features",
    )

    phase = models.ForeignKey(
        Phase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="features",
    )

    name = models.CharField(max_length=300)

    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="backend",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    user_facing = models.BooleanField(default=True)

    acceptance_criteria = models.TextField(blank=True)

    target_release = models.CharField(
        max_length=100,
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="features",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# TASK
# =========================================================

class Task(models.Model):
    """
    Main executable work item.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )

    feature = models.ForeignKey(
        Feature,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pm_tasks",
    )

    task_code = models.CharField(
        max_length=20,
        unique=True,
    )

    title = models.CharField(max_length=300)

    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="backend",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    target_file = models.CharField(
        max_length=500,
        blank=True,
    )

    estimated_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    actual_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    ai_generated = models.BooleanField(default=False)

    ai_summary = models.TextField(blank=True)

    ai_risk_score = models.FloatField(default=0)

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tasks",
    )

    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "task_code"]

    def __str__(self):
        return f"[{self.task_code}] {self.title}"

    @property
    def subtask_progress(self):
        total = self.subtasks.count()

        if total == 0:
            return "0/0"

        completed = self.subtasks.filter(
            status="completed"
        ).count()

        return f"{completed}/{total}"


# =========================================================
# SUBTASK
# =========================================================

class SubTask(models.Model):
    """
    Small checklist items.
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )

    title = models.CharField(max_length=300)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title


# =========================================================
# TASK DEPENDENCY
# =========================================================

class TaskDependency(models.Model):
    """
    Dependency graph between tasks.
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="dependencies",
    )

    depends_on = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="dependents",
    )

    class Meta:
        unique_together = [
            ("task", "depends_on")
        ]

    def __str__(self):
        return (
            f"{self.task.task_code} "
            f"depends on "
            f"{self.depends_on.task_code}"
        )


# =========================================================
# DOCUMENTATION
# =========================================================

class Documentation(models.Model):
    """
    Documentation tracking.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="docs",
    )

    title = models.CharField(max_length=300)

    file_path = models.CharField(max_length=500)

    doc_type = models.CharField(
        max_length=50,
        default="overview",
    )

    status = models.CharField(
        max_length=20,
        choices=DOC_STATUS_CHOICES,
        default="missing",
    )

    completeness = models.PositiveIntegerField(default=0)

    notes = models.TextField(blank=True)

    last_reviewed = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


# =========================================================
# TECH DEBT
# =========================================================

class TechDebt(models.Model):
    """
    Technical debt tracking.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tech_debts",
    )

    title = models.CharField(max_length=300)

    description = models.TextField(blank=True)

    severity = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    affected_files = models.TextField(blank=True)

    impact = models.TextField(blank=True)

    remediation = models.TextField(blank=True)

    estimated_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# =========================================================
# DEPLOYMENT
# =========================================================

class Deployment(models.Model):
    """
    Environment deployment tracking.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="deployments",
    )

    environment = models.CharField(
        max_length=20,
        choices=ENVIRONMENT_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    version = models.CharField(
        max_length=100,
        blank=True,
    )

    url = models.URLField(blank=True)

    health_check_url = models.URLField(blank=True)

    deployed_by = models.CharField(
        max_length=100,
        blank=True,
    )

    notes = models.TextField(blank=True)

    last_deployed = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [
            ("project", "environment")
        ]

    def __str__(self):
        return (
            f"{self.project.name} - "
            f"{self.environment}"
        )


# =========================================================
# AI MEMORY
# =========================================================

class AIMemory(models.Model):
    """
    Long-term AI memory/context storage.
    Useful for:
    - RAG
    - agent memory
    - architecture summaries
    - PM intelligence
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="ai_memories",
    )

    title = models.CharField(max_length=300)

    memory_type = models.CharField(
        max_length=100,
        default="general",
    )

    content = models.TextField()

    embedding_id = models.CharField(
        max_length=200,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# =========================================================
# AI INSIGHT
# =========================================================

class AIInsight(models.Model):
    """
    AI-generated operational/project insights.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="ai_insights",
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    insight_type = models.CharField(
        max_length=100,
    )

    severity = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    title = models.CharField(max_length=300)

    description = models.TextField()

    recommendation = models.TextField(blank=True)

    resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title