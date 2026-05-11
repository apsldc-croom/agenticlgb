"""
pm/management/commands/seed_pm.py

Seed the PM database with SLDC Grid Ops project data.

Usage:
    python manage.py seed_pm
    python manage.py seed_pm --flush
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from pm.models import (
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
    TechDebt,
)


class Command(BaseCommand):
    help = "Seed the PM database with SLDC Grid Ops project data."

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

        self.stdout.write("Seeding SLDC Grid Ops PM data...")

        # ── Tags ──
        tags = {}
        for name, color in [
            ("backend", "#3b82f6"),
            ("frontend", "#8b5cf6"),
            ("devops", "#f59e0b"),
            ("ai", "#10b981"),
            ("docs", "#6b7280"),
            ("testing", "#ef4444"),
            ("security", "#dc2626"),
            ("infra", "#0891b2"),
            ("database", "#f97316"),
            ("api", "#06b6d4"),
            ("telemetry", "#14b8a6"),
            ("forecasting", "#a855f7"),
            ("scheduling", "#ec4899"),
            ("market", "#eab308"),
        ]:
            tags[name], _ = Tag.objects.get_or_create(
                name=name, defaults={"color": color}
            )

        # ── Project ──
        project, created = Project.objects.get_or_create(
            slug="sldc-grid-ops",
            defaults={
                "name": "SLDC Grid Ops",
                "tagline": "AI-Native Power Grid Operational Intelligence Platform",
                "vision": (
                    "Build a production-grade SLDC operational intelligence platform "
                    "combining real-time telemetry, load forecasting, market analytics, "
                    "and agentic AI for grid dispatch optimization across AP Transco."
                ),
                "description": (
                    "Power grid operations platform with demand forecasting, "
                    "generator scheduling, market watch, scenario analysis, "
                    "dispatch control, and AI-powered decision support."
                ),
                "status": "in_progress",
                "priority": "critical",
                "repo_url": "https://github.com/apsldc-croom/agenticlgb",
                "tech_stack": [
                    "Django 5.1", "DRF", "React 18", "Vite",
                    "PostgreSQL 16", "Redis 7", "Celery",
                    "Docker", "Nginx", "GitHub Actions",
                ],
                "metadata": {
                    "organization": "AP Transco SLDC",
                    "total_phases": 7,
                    "architecture": "Monolith-first, service-ready",
                },
            },
        )

        if not created:
            self.stdout.write(self.style.WARNING(
                "Project 'sldc-grid-ops' exists. Updating..."
            ))

        self.stdout.write(f"Project: {project}")

        # ── Goals ──
        goals_data = [
            {
                "title": "Production VM Deployment",
                "description": "Full Docker stack on GCP VM with CI/CD",
                "priority": "critical",
                "status": "in_progress",
                "target_metric": "Uptime",
                "current_value": "85%",
                "target_value": "99.5%",
            },
            {
                "title": "Real-time Grid Telemetry Dashboard",
                "description": "Live frequency, demand, and generator status",
                "priority": "critical",
                "status": "planning",
                "target_metric": "Data latency",
                "current_value": "5min",
                "target_value": "<15s",
            },
            {
                "title": "Demand Forecasting Engine",
                "description": "ML-based load forecasting (day-ahead, intra-day)",
                "priority": "high",
                "status": "planning",
                "target_metric": "MAPE",
                "current_value": "N/A",
                "target_value": "<3%",
            },
            {
                "title": "Market Analytics & IEX Integration",
                "description": "Real-time IEX price feeds and trading analytics",
                "priority": "high",
                "status": "in_progress",
                "target_metric": "Price accuracy",
                "current_value": "80%",
                "target_value": "99%",
            },
            {
                "title": "Agentic AI Dispatch Advisor",
                "description": "AI agent for optimal generator scheduling",
                "priority": "medium",
                "status": "planning",
                "target_metric": "Cost savings",
                "current_value": "0",
                "target_value": "5% reduction",
            },
        ]
        for i, g in enumerate(goals_data):
            Goal.objects.get_or_create(
                project=project, title=g["title"],
                defaults={**g, "sort_order": i},
            )

        # ── Phases ──
        phases_data = [
            (1, "Infrastructure & DevOps",
             "Docker, CI/CD, VM deployment, Nginx, PostgreSQL, Redis", 2,
             "in_progress"),
            (2, "Core Platform & Auth",
             "Custom User model, JWT auth, PM module, admin panel", 2,
             "in_progress"),
            (3, "Data Pipeline & Telemetry",
             "SCADA ingestion, energy meter parsing, daily aggregates", 3,
             "in_progress"),
            (4, "Market & Scheduling",
             "IEX price feeds, generator scheduling, dispatch optimization", 3,
             "planning"),
            (5, "Forecasting & Analytics",
             "Load forecasting ML, demand prediction, trend analysis", 4,
             "planning"),
            (6, "Frontend Dashboard Suite",
             "Grid ops dashboard, market watch, scenario builder UI", 3,
             "in_progress"),
            (7, "AI & Intelligence Layer",
             "Agentic AI, RAG, knowledge graph, decision support", 4,
             "planning"),
        ]
        phases = {}
        for num, name, desc, weeks, st in phases_data:
            phase, _ = Phase.objects.get_or_create(
                project=project, phase_number=num,
                defaults={
                    "name": name, "description": desc,
                    "duration_weeks": weeks, "status": st,
                    "sort_order": num,
                },
            )
            phases[num] = phase

        # ── Tasks ──
        tasks_raw = [
            # Phase 1: Infrastructure
            (1, "SLDC-001", "Write Dockerfile.backend (multi-stage)", "critical",
             "devops", "docker/Dockerfile.backend", 2, "completed"),
            (1, "SLDC-002", "Write Dockerfile.frontend (Nginx + Vite build)", "critical",
             "devops", "docker/Dockerfile.frontend", 2, "completed"),
            (1, "SLDC-003", "Write docker-compose.prod.yml", "critical",
             "devops", "docker-compose.prod.yml", 3, "completed"),
            (1, "SLDC-004", "Configure Nginx reverse proxy with dynamic DNS", "critical",
             "infra", "docker/nginx/app.conf", 2, "completed"),
            (1, "SLDC-005", "Set up GitHub Actions CI (lint + test + build)", "high",
             "devops", ".github/workflows/ci.yml", 2, "completed"),
            (1, "SLDC-006", "Set up GitHub Actions CD (SSH deploy)", "high",
             "devops", ".github/workflows/cd.yml", 2, "completed"),
            (1, "SLDC-007", "Configure production.py settings", "critical",
             "backend", "src/config/settings/production.py", 1, "completed"),
            (1, "SLDC-008", "Set up GCP VM with Docker + Git", "high",
             "infra", "", 3, "completed"),
            (1, "SLDC-009", "Configure Celery + Redis worker", "medium",
             "backend", "docker/Dockerfile.worker", 2, "completed"),
            (1, "SLDC-010", "SSL/TLS certificate (Let's Encrypt)", "medium",
             "infra", "", 1, "not_started"),

            # Phase 2: Core Platform
            (2, "SLDC-020", "Custom User model (email-based, RBAC)", "critical",
             "backend", "src/core/users/models.py", 2, "completed"),
            (2, "SLDC-021", "JWT auth with enriched token response", "critical",
             "backend", "src/core/users/views.py", 2, "completed"),
            (2, "SLDC-022", "PM module models (Project, Phase, Task, etc.)", "critical",
             "backend", "src/pm/models.py", 4, "completed"),
            (2, "SLDC-023", "PM API ViewSets + serializers", "critical",
             "backend", "src/pm/views.py", 3, "completed"),
            (2, "SLDC-024", "Task audit history (signals + immutable log)", "high",
             "backend", "src/pm/signals.py", 2, "completed"),
            (2, "SLDC-025", "Seed PM data management command", "medium",
             "backend", "src/pm/management/commands/seed_pm.py", 2, "in_progress"),
            (2, "SLDC-026", "Django Admin configuration", "low",
             "backend", "src/pm/admin.py", 1, "not_started"),

            # Phase 3: Data Pipeline
            (3, "SLDC-030", "SCADA data ingestion service", "critical",
             "backend", "src/telemetry/services/scada.py", 4, "in_progress"),
            (3, "SLDC-031", "Energy meter Excel parser", "critical",
             "backend", "src/telemetry/services/energy_meter.py", 3, "completed"),
            (3, "SLDC-032", "Daily aggregate pipeline (MU computation)", "critical",
             "backend", "src/telemetry/services/aggregation.py", 4, "in_progress"),
            (3, "SLDC-033", "Gmail attachment auto-fetch (energy reports)", "high",
             "backend", "src/telemetry/services/gmail_fetch.py", 3, "completed"),
            (3, "SLDC-034", "Generator master data management", "high",
             "database", "src/telemetry/models.py", 2, "completed"),
            (3, "SLDC-035", "Schedule model + import pipeline", "high",
             "backend", "src/scheduling/services/import.py", 3, "in_progress"),
            (3, "SLDC-036", "Telemetry health check endpoint", "medium",
             "backend", "src/telemetry/views.py", 1, "not_started"),

            # Phase 4: Market & Scheduling
            (4, "SLDC-040", "IEX price feed integration", "critical",
             "backend", "src/market/services/iex.py", 4, "in_progress"),
            (4, "SLDC-041", "Market price aggregation (DAM/RTM)", "high",
             "backend", "src/market/services/aggregation.py", 3, "planning"),
            (4, "SLDC-042", "Generator scheduling optimizer", "critical",
             "backend", "src/scheduling/services/optimizer.py", 6, "planning"),
            (4, "SLDC-043", "Dispatch control API endpoints", "high",
             "backend", "src/scheduling/views.py", 3, "planning"),
            (4, "SLDC-044", "Cost curve modeling for generators", "high",
             "ai", "src/scheduling/services/cost_curves.py", 4, "planning"),
            (4, "SLDC-045", "Inter-state power exchange tracking", "medium",
             "backend", "src/market/services/exchange.py", 3, "not_started"),

            # Phase 5: Forecasting
            (5, "SLDC-050", "Day-ahead load forecast model", "critical",
             "ai", "src/forecasting/models/day_ahead.py", 6, "planning"),
            (5, "SLDC-051", "Intra-day demand prediction", "high",
             "ai", "src/forecasting/models/intra_day.py", 4, "planning"),
            (5, "SLDC-052", "Weather data integration (IMD API)", "high",
             "backend", "src/forecasting/services/weather.py", 3, "planning"),
            (5, "SLDC-053", "Forecast accuracy evaluation pipeline", "medium",
             "ai", "src/forecasting/evaluation/runner.py", 3, "not_started"),
            (5, "SLDC-054", "Historical trend analysis service", "medium",
             "backend", "src/analytics/services/trends.py", 2, "not_started"),

            # Phase 6: Frontend
            (6, "SLDC-060", "Login page with JWT auth flow", "critical",
             "frontend", "src/pages/Auth/Login.tsx", 2, "completed"),
            (6, "SLDC-061", "PM Dashboard (phases, tasks, features)", "critical",
             "frontend", "src/pages/PM/PMDashboard.tsx", 4, "in_progress"),
            (6, "SLDC-062", "PM Tasks list with bulk updates", "high",
             "frontend", "src/pages/PM/PMTasks.tsx", 3, "completed"),
            (6, "SLDC-063", "Market Watch dashboard", "high",
             "frontend", "src/pages/MarketWatch/", 4, "planning"),
            (6, "SLDC-064", "Dispatch Control interface", "high",
             "frontend", "src/pages/DispatchControl/", 4, "planning"),
            (6, "SLDC-065", "Scenario Builder UI", "medium",
             "frontend", "src/pages/ScenarioBuilder/", 3, "planning"),
            (6, "SLDC-066", "Home/Landing page", "medium",
             "frontend", "src/pages/Home/", 2, "in_progress"),

            # Phase 7: AI
            (7, "SLDC-070", "LLM provider abstraction layer", "high",
             "ai", "src/intelligence/providers/", 3, "planning"),
            (7, "SLDC-071", "Grid ops RAG pipeline", "high",
             "ai", "src/intelligence/rag/pipeline.py", 5, "planning"),
            (7, "SLDC-072", "Dispatch advisor agent", "critical",
             "ai", "src/intelligence/agents/dispatch.py", 6, "planning"),
            (7, "SLDC-073", "Anomaly detection for grid metrics", "high",
             "ai", "src/intelligence/anomaly/detector.py", 4, "planning"),
            (7, "SLDC-074", "Knowledge graph for grid topology", "medium",
             "ai", "src/intelligence/graph/builder.py", 4, "not_started"),
        ]

        task_objs = {}
        for ph, code, title, prio, cat, target, hours, st in tasks_raw:
            task, cr = Task.objects.get_or_create(
                task_code=code,
                defaults={
                    "project": project,
                    "phase": phases[ph],
                    "title": title,
                    "priority": prio,
                    "status": st,
                    "category": cat,
                    "target_file": target,
                    "estimated_hours": hours,
                    "sort_order": int(code.split("-")[1]),
                },
            )
            if cr and cat in tags:
                task.tags.add(tags[cat])
            task_objs[code] = task

        # Add subtasks to in_progress tasks
        for code, task in task_objs.items():
            if task.status == "in_progress" and not task.subtasks.exists():
                SubTask.objects.create(task=task, title=f"Design: {task.title}",
                                       status="completed", sort_order=1)
                SubTask.objects.create(task=task, title=f"Implement: {task.title}",
                                       status="in_progress", sort_order=2)
                SubTask.objects.create(task=task, title=f"Test: {task.title}",
                                       status="not_started", sort_order=3)

        # ── Milestones ──
        milestones = [
            (1, "Docker stack live on VM", "All containers healthy on 34.93.126.189"),
            (1, "CI/CD pipelines active", "GitHub Actions auto-deploy on push to main"),
            (2, "Auth + PM module operational", "JWT login + full PM CRUD working"),
            (3, "Daily pipeline automated", "SCADA + Energy Meter → aggregates → DB"),
            (4, "Market feed live", "IEX DAM/RTM prices updating every 15min"),
            (5, "First forecast model deployed", "Day-ahead MAPE < 5%"),
            (6, "Dashboard suite MVP", "PM + Market + Dispatch pages live"),
            (7, "AI advisor prototype", "Dispatch recommendation agent working"),
        ]
        for ph, title, deliv in milestones:
            Milestone.objects.get_or_create(
                phase=phases[ph], title=title,
                defaults={"deliverable": deliv},
            )

        # ── Features ──
        features = [
            ("JWT Authentication (Email-based)", "completed", "critical",
             "backend", True, 2),
            ("Custom User Model + RBAC", "completed", "critical",
             "backend", False, 2),
            ("PM Dashboard & Task Management", "in_progress", "critical",
             "frontend", True, 6),
            ("Docker Production Stack", "completed", "critical",
             "devops", False, 1),
            ("CI/CD Pipeline (GitHub Actions)", "completed", "high",
             "devops", False, 1),
            ("SCADA Data Ingestion", "in_progress", "critical",
             "backend", False, 3),
            ("Energy Meter Import", "completed", "high",
             "backend", False, 3),
            ("IEX Market Price Feed", "in_progress", "high",
             "backend", True, 4),
            ("Market Watch Dashboard", "planning", "high",
             "frontend", True, 6),
            ("Day-Ahead Load Forecasting", "planning", "critical",
             "ai", True, 5),
            ("Generator Scheduling Optimizer", "planning", "critical",
             "backend", True, 4),
            ("Dispatch Control Interface", "planning", "high",
             "frontend", True, 6),
            ("Scenario Builder", "planning", "medium",
             "frontend", True, 6),
            ("Grid Anomaly Detection", "planning", "high",
             "ai", False, 7),
            ("AI Dispatch Advisor Agent", "planning", "high",
             "ai", True, 7),
        ]
        for name, st, prio, cat, uf, ph in features:
            Feature.objects.get_or_create(
                project=project, name=name,
                defaults={
                    "status": st, "priority": prio,
                    "category": cat, "user_facing": uf,
                    "phase": phases.get(ph),
                },
            )

        # ── Architecture Layers ──
        layers = [
            (1, "Core Config & Settings", "src/config/", "in_progress"),
            (2, "Auth & Users", "src/core/users/", "completed"),
            (3, "PM Module", "src/pm/", "in_progress"),
            (4, "Telemetry & SCADA", "src/telemetry/", "in_progress"),
            (5, "Market Analytics", "src/market/", "planning"),
            (6, "Scheduling & Dispatch", "src/scheduling/", "planning"),
            (7, "Forecasting Engine", "src/forecasting/", "planning"),
            (8, "Intelligence (AI/RAG)", "src/intelligence/", "planning"),
            (9, "Analytics & Reports", "src/analytics/", "planning"),
            (10, "Background Workers", "src/worker/", "in_progress"),
            (11, "Frontend SPA", "LGB-frontend/src/", "in_progress"),
            (12, "DevOps & CI/CD", "docker/ + .github/", "completed"),
        ]
        for num, name, directory, st in layers:
            ArchitectureLayer.objects.get_or_create(
                project=project, layer_number=num,
                defaults={
                    "name": name, "directory": directory, "status": st,
                },
            )

        # ── Documentation ──
        docs = [
            ("System Architecture", "docs/architecture.md", "overview",
             "draft", 40),
            ("API Reference", "docs/api-reference.md", "api", "missing", 0),
            ("Deployment Guide", "docs/deployment.md", "guide", "draft", 60),
            ("Data Pipeline Docs", "docs/data-pipeline.md", "guide",
             "draft", 35),
            ("PM Module README", "docs/pm-module.md", "overview",
             "published", 80),
            ("Generator Master Data", "docs/generators.md", "reference",
             "draft", 50),
            ("Market Integration", "docs/market-integration.md", "guide",
             "missing", 0),
            ("AI Architecture ADR", "docs/decisions/adr-ai.md", "adr",
             "missing", 0),
        ]
        for title, path, dtype, st, comp in docs:
            Documentation.objects.get_or_create(
                project=project, title=title,
                defaults={
                    "file_path": path, "doc_type": dtype,
                    "status": st, "completeness": comp,
                },
            )

        # ── Tech Debt ──
        debts = [
            ("No unit tests for PM module", "high", "testing",
             "Low confidence in refactors", "src/pm/tests/"),
            ("Hardcoded DB credentials in dev.py", "medium", "security",
             "Credential leak risk", "src/config/settings/dev.py"),
            ("Frontend bundle > 500KB", "low", "frontend",
             "Slow initial load on mobile", "LGB-frontend/vite.config.ts"),
            ("No API rate limiting", "high", "security",
             "Vulnerable to abuse", "src/config/settings/base.py"),
            ("Raw SQL in aggregation service", "medium", "backend",
             "SQL injection risk, hard to maintain",
             "src/telemetry/services/aggregation.py"),
        ]
        for title, sev, cat, impact, files in debts:
            TechDebt.objects.get_or_create(
                project=project, title=title,
                defaults={
                    "severity": sev, "impact": impact,
                    "affected_files": files,
                },
            )

        # ── Deployments ──
        Deployment.objects.get_or_create(
            project=project, environment="production",
            defaults={
                "status": "in_progress",
                "version": "0.1.0",
                "url": "http://34.93.126.189",
                "health_check_url": "http://34.93.126.189/api/health/",
                "deployed_by": "GitHub Actions",
                "last_deployed": timezone.now(),
            },
        )
        Deployment.objects.get_or_create(
            project=project, environment="local",
            defaults={
                "status": "completed",
                "version": "0.1.0-dev",
                "url": "http://localhost:5173",
                "deployed_by": "manual",
            },
        )

        # ── Summary ──
        completed = Task.objects.filter(
            project=project, status="completed"
        ).count()
        total = Task.objects.filter(project=project).count()

        self.stdout.write(self.style.SUCCESS(
            f"\n{'='*50}\n"
            f"  SLDC Grid Ops — Seed Complete\n"
            f"  {total} tasks ({completed} completed)\n"
            f"  {len(phases_data)} phases\n"
            f"  {len(features)} features\n"
            f"  {len(layers)} architecture layers\n"
            f"  {len(docs)} docs · {len(debts)} tech debts\n"
            f"  2 deployments\n"
            f"{'='*50}"
        ))
