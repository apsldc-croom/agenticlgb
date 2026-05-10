"""
pm/serializers.py

DRF Serializers for all PM models.
-----------------------------------
Includes:
- List serializers (lightweight)
- Detail serializers (full fields + nested reads)
- Write serializers (for create/update)
"""

from rest_framework import serializers

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


# =========================================================
# TAG
# =========================================================

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color"]


# =========================================================
# GOAL
# =========================================================

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id", "project", "title", "description",
            "priority", "status",
            "target_metric", "current_value", "target_value",
            "due_date", "sort_order",
        ]


# =========================================================
# MILESTONE
# =========================================================

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = [
            "id", "phase", "title", "description",
            "deliverable", "status", "target_date",
        ]


# =========================================================
# SUBTASK
# =========================================================

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            "id", "task", "title", "description",
            "status", "sort_order",
        ]


# =========================================================
# TASK STATUS HISTORY
# =========================================================

class TaskStatusHistorySerializer(serializers.ModelSerializer):
    """Read-only audit trail of task status transitions."""
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = TaskStatusHistory
        fields = [
            "id", "task",
            "from_status", "to_status",
            "changed_by", "changed_by_name",
            "changed_at", "note",
        ]
        read_only_fields = fields

    def get_changed_by_name(self, obj):
        if obj.changed_by:
            return obj.changed_by.get_full_name()
        return "system"


# =========================================================
# TASK DEPENDENCY
# =========================================================

class TaskDependencySerializer(serializers.ModelSerializer):
    task_code = serializers.CharField(
        source="task.task_code",
        read_only=True,
    )
    depends_on_code = serializers.CharField(
        source="depends_on.task_code",
        read_only=True,
    )

    class Meta:
        model = TaskDependency
        fields = [
            "id", "task", "depends_on",
            "task_code", "depends_on_code",
        ]


# =========================================================
# ARCHITECTURE LAYER
# =========================================================

class ArchitectureLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectureLayer
        fields = [
            "id", "project", "layer_number", "name",
            "description", "directory", "owner",
            "status", "dependencies", "notes",
        ]


# =========================================================
# DOCUMENTATION
# =========================================================

class DocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = [
            "id", "project", "title", "file_path",
            "doc_type", "status", "completeness",
            "notes", "last_reviewed",
        ]


# =========================================================
# TECH DEBT
# =========================================================

class TechDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechDebt
        fields = [
            "id", "project", "title", "description",
            "severity", "status", "affected_files",
            "impact", "remediation", "estimated_hours",
            "created_at",
        ]
        read_only_fields = ["created_at"]


# =========================================================
# DEPLOYMENT
# =========================================================

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = [
            "id", "project", "environment", "status",
            "version", "url", "health_check_url",
            "deployed_by", "notes", "last_deployed",
        ]


# =========================================================
# AI MEMORY
# =========================================================

class AIMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMemory
        fields = [
            "id", "project", "title", "memory_type",
            "content", "embedding_id", "metadata",
            "created_at",
        ]
        read_only_fields = ["created_at"]


# =========================================================
# AI INSIGHT
# =========================================================

class AIInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInsight
        fields = [
            "id", "project", "task", "insight_type",
            "severity", "title", "description",
            "recommendation", "resolved", "created_at",
        ]
        read_only_fields = ["created_at"]


# =========================================================
# FEATURE
# =========================================================

class FeatureListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Feature
        fields = [
            "id", "project", "phase", "name",
            "category", "priority", "status",
            "user_facing", "tags", "created_at",
        ]
        read_only_fields = ["created_at"]


class FeatureDetailSerializer(serializers.ModelSerializer):
    """Full serializer with all fields."""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source="tags",
        required=False,
    )

    class Meta:
        model = Feature
        fields = [
            "id", "project", "phase", "name",
            "description", "category", "priority", "status",
            "user_facing", "acceptance_criteria",
            "target_release", "tags", "tag_ids",
            "created_at",
        ]
        read_only_fields = ["created_at"]


# =========================================================
# TASK
# =========================================================

class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight task serializer for list views."""
    tags = TagSerializer(many=True, read_only=True)
    subtask_progress = serializers.CharField(read_only=True)
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "task_code", "title",
            "project", "phase", "category",
            "priority", "status",
            "assigned_to", "assigned_to_name",
            "due_date", "subtask_progress",
            "ai_generated", "tags",
            "sort_order", "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name()
        return None


class TaskDetailSerializer(serializers.ModelSerializer):
    """Full task serializer with nested subtasks, dependencies and status history."""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source="tags",
        required=False,
    )
    subtasks = SubTaskSerializer(many=True, read_only=True)
    dependencies = TaskDependencySerializer(many=True, read_only=True)
    status_history = TaskStatusHistorySerializer(many=True, read_only=True)
    subtask_progress = serializers.CharField(read_only=True)
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "task_code", "title", "description",
            "project", "phase", "milestone", "feature",
            "category", "priority", "status",
            "assigned_to", "assigned_to_name",
            "target_file",
            "estimated_hours", "actual_hours",
            "ai_generated", "ai_summary", "ai_risk_score",
            "due_date", "completed_at",
            "tags", "tag_ids",
            "subtasks", "dependencies",
            "status_history",
            "subtask_progress",
            "sort_order", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name()
        return None


# =========================================================
# PHASE (with nested milestone + task counts)
# =========================================================

class PhaseListSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.FloatField(read_only=True)
    task_count = serializers.SerializerMethodField()
    milestone_count = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = [
            "id", "project", "phase_number", "name",
            "status", "start_date", "end_date",
            "duration_weeks", "sort_order",
            "progress_percentage",
            "task_count", "milestone_count",
        ]

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_milestone_count(self, obj):
        return obj.milestones.count()


class PhaseDetailSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    features = FeatureListSerializer(many=True, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Phase
        fields = [
            "id", "project", "phase_number", "name",
            "description", "status",
            "start_date", "end_date", "duration_weeks",
            "architecture_layers", "sort_order",
            "progress_percentage",
            "milestones", "features",
        ]


# =========================================================
# PROJECT (top-level with counts)
# =========================================================

class ProjectListSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.FloatField(read_only=True)
    phase_count = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "name", "slug", "tagline",
            "status", "priority",
            "start_date", "target_end_date",
            "progress_percentage",
            "phase_count", "task_count",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_phase_count(self, obj):
        return obj.phases.count()

    def get_task_count(self, obj):
        return obj.tasks.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    phases = PhaseListSerializer(many=True, read_only=True)
    goals = GoalSerializer(many=True, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "name", "slug", "tagline",
            "vision", "description",
            "status", "priority",
            "repo_url", "documentation_url",
            "tech_stack", "metadata",
            "created_by",
            "start_date", "target_end_date",
            "progress_percentage",
            "phases", "goals",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
