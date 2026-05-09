"""
pm/management/commands/seed_pm.py

Management command to seed the PM database with sample data
for development and testing.

Usage:
    python manage.py seed_pm
    python manage.py seed_pm --flush  # Clear existing data first
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

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
)


class Command(BaseCommand):
    help = "Seed the PM database with sample project data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing PM data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing PM data...")
            Project.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write(self.style.WARNING("All PM data deleted."))

        self.stdout.write("Seeding PM data...")

        # --- Tags ---
        tags = {}
        tag_data = [
            ("auth", "#ef4444"),
            ("ai", "#8b5cf6"),
            ("rag", "#6366f1"),
            ("websocket", "#10b981"),
            ("database", "#f59e0b"),
            ("api", "#3b82f6"),
            ("security", "#dc2626"),
            ("devops", "#14b8a6"),
            ("frontend", "#ec4899"),
            ("testing", "#84cc16"),
        ]
        for name, color in tag_data:
            tag, _ = Tag.objects.get_or_create(
                name=name,
                defaults={"color": color},
            )
            tags[name] = tag

        # --- Project ---
        project, created = Project.objects.get_or_create(
            slug="lgb-platform",
            defaults={
                "name": "LGB Platform",
                "tagline": "AI-Native Learning & Growth Platform",
                "vision": (
                    "Build an intelligent community platform that leverages "
                    "AI to enhance learning, collaboration, and growth."
                ),
                "status": "in_progress",
                "priority": "critical",
                "tech_stack": [
                    "Django", "DRF", "PostgreSQL", "Redis",
                    "Celery", "Next.js", "OpenAI", "pgvector",
                ],
            },
        )

        if not created:
            self.stdout.write(
                self.style.WARNING("Project 'lgb-platform' already exists, skipping.")
            )
            return

        # --- Goals ---
        Goal.objects.create(
            project=project,
            title="Launch MVP",
            description="Ship core platform with auth, forums, and groups.",
            priority="critical",
            target_metric="Active users",
            target_value="100",
            sort_order=1,
        )
        Goal.objects.create(
            project=project,
            title="Integrate AI Assistant",
            description="Deploy RAG-powered AI assistant for platform queries.",
            priority="high",
            target_metric="Query accuracy",
            target_value="90%",
            sort_order=2,
        )

        # --- Phases ---
        phases = []
        phase_data = [
            (1, "Foundation", "Core infrastructure: auth, database, project structure", 3),
            (2, "Core Platform", "Users, groups, forums, events", 4),
            (3, "Social Layer", "Chat, notifications, media uploads", 3),
            (4, "AI Foundation", "LLM providers, prompts, basic AI services", 4),
            (5, "Advanced RAG", "Document ingestion, vector search, RAG pipeline", 4),
            (6, "Agentic Systems", "Multi-agent orchestration, knowledge graph", 6),
            (7, "Observability", "Logging, metrics, tracing, health checks", 2),
            (8, "Enterprise Hardening", "Security audit, performance optimization", 3),
            (9, "Scale & Optimization", "Caching, read replicas, CDN", 2),
        ]
        for num, name, desc, weeks in phase_data:
            p = Phase.objects.create(
                project=project,
                phase_number=num,
                name=name,
                description=desc,
                duration_weeks=weeks,
                status="completed" if num == 1 else (
                    "in_progress" if num == 2 else "planning"
                ),
            )
            phases.append(p)

        # --- Milestones ---
        Milestone.objects.create(
            phase=phases[0],
            title="Project structure verified",
            status="completed",
        )
        Milestone.objects.create(
            phase=phases[1],
            title="User registration and auth working",
            status="in_progress",
        )
        Milestone.objects.create(
            phase=phases[3],
            title="First AI response in platform",
            status="planning",
        )

        # --- Architecture Layers ---
        layers = [
            (1, "API Gateway", "src/config/"),
            (2, "Authentication", "src/apps/users/"),
            (3, "Domain Apps", "src/apps/"),
            (4, "AI Subsystem", "src/ai/"),
            (5, "Worker", "src/worker/"),
            (6, "Observability", "src/observability/"),
        ]
        for num, name, directory in layers:
            ArchitectureLayer.objects.create(
                project=project,
                layer_number=num,
                name=name,
                directory=directory,
            )

        # --- Features ---
        f_auth = Feature.objects.create(
            project=project,
            phase=phases[0],
            name="JWT Authentication",
            category="backend",
            priority="critical",
            status="completed",
        )
        f_auth.tags.add(tags["auth"], tags["api"], tags["security"])

        f_forums = Feature.objects.create(
            project=project,
            phase=phases[1],
            name="Forum Threads",
            category="backend",
            priority="high",
            status="in_progress",
        )
        f_forums.tags.add(tags["api"])

        f_ai = Feature.objects.create(
            project=project,
            phase=phases[3],
            name="AI Assistant",
            category="ai_ml",
            priority="high",
            status="planning",
        )
        f_ai.tags.add(tags["ai"], tags["rag"])

        # --- Tasks ---
        task_data = [
            ("LGB-001", "Set up Django project structure", phases[0], "completed", "backend", tags["api"]),
            ("LGB-002", "Configure JWT authentication", phases[0], "completed", "security", tags["auth"]),
            ("LGB-003", "Create User model", phases[1], "completed", "backend", tags["auth"]),
            ("LGB-004", "Build Forum CRUD API", phases[1], "in_progress", "backend", tags["api"]),
            ("LGB-005", "Implement Group management", phases[1], "planning", "backend", tags["api"]),
            ("LGB-006", "Set up OpenAI provider", phases[3], "planning", "ai_ml", tags["ai"]),
            ("LGB-007", "Build RAG pipeline", phases[4], "planning", "ai_ml", tags["rag"]),
            ("LGB-008", "WebSocket chat", phases[2], "planning", "backend", tags["websocket"]),
            ("LGB-009", "Set up Celery workers", phases[0], "completed", "devops", tags["devops"]),
            ("LGB-010", "Database schema review", phases[1], "review", "database", tags["database"]),
        ]

        for code, title, phase, task_status, category, tag in task_data:
            t = Task.objects.create(
                project=project,
                phase=phase,
                task_code=code,
                title=title,
                status=task_status,
                category=category,
            )
            t.tags.add(tag)

            # Add subtasks to in-progress tasks
            if task_status == "in_progress":
                SubTask.objects.create(
                    task=t,
                    title=f"Design {title}",
                    status="completed",
                    sort_order=1,
                )
                SubTask.objects.create(
                    task=t,
                    title=f"Implement {title}",
                    status="in_progress",
                    sort_order=2,
                )
                SubTask.objects.create(
                    task=t,
                    title=f"Test {title}",
                    status="not_started",
                    sort_order=3,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"[OK] Seeded: 1 project, {len(phases)} phases, "
                f"{len(task_data)} tasks, {len(tag_data)} tags"
            )
        )
