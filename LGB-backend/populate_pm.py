import os
import sys
import django

# Setup Django path and settings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from pm.models import Project, Phase, Task

def populate():
    print("Creating Project...")
    project, created = Project.objects.get_or_create(
        slug="sldc-grid-ops",
        defaults={
            "name": "SLDC Power Grid Optimization",
            "tagline": "Operational Intelligence and Analytics Platform",
            "status": "in_progress",
        }
    )

    phases_data = [
        {
            "phase_number": 1,
            "name": "Problem Formalisation",
            "description": "Formalize domain models and objectives",
            "status": "completed",
            "tasks": [
                ("1.1", "Define SLDC domain models (Generators, Network, Market, etc.)", "docs", "completed"),
                ("1.2", "Formalise optimization objectives (Cost minimization)", "docs", "completed"),
                ("1.3", "Draft non-functional requirements", "docs", "completed"),
            ]
        },
        {
            "phase_number": 2,
            "name": "Data Infrastructure",
            "description": "Establish data pipelines and integrations",
            "status": "in_progress",
            "tasks": [
                ("2.1", "Implement Gmail Excel import service for market data", "backend", "completed"),
                ("2.2", "Establish Energy Meter robust ingestion pipeline", "backend", "completed"),
                ("2.3", "Refactor aggregation into domain-specific modules", "backend", "completed"),
                ("2.4", "Integrate SCADA telemetry data pipelines", "backend", "in_progress"),
            ]
        },
        {
            "phase_number": 3,
            "name": "Optimisation Engine",
            "description": "Core grid optimization logic",
            "status": "planning",
            "tasks": [
                ("3.1", "Develop Generator dispatch optimization logic", "ai_ml", "planning"),
                ("3.2", "Implement Network constraint modeling", "backend", "planning"),
                ("3.3", "Build Market cost minimization algorithms", "ai_ml", "planning"),
                ("3.4", "Integrate Forecasting models for load", "ai_ml", "planning"),
            ]
        },
        {
            "phase_number": 4,
            "name": "Scenario Engine",
            "description": "What-if analysis and backtesting",
            "status": "planning",
            "tasks": [
                ("4.1", "Create base scenario management system", "backend", "planning"),
                ("4.2", "Implement comparative analysis", "backend", "planning"),
                ("4.3", "Build historical simulation backtesting", "backend", "planning"),
            ]
        },
        {
            "phase_number": 5,
            "name": "Operational Intelligence Layer",
            "description": "Real-time insights and auth",
            "status": "in_progress",
            "tasks": [
                ("5.1", "Implement JWT Authentication and AuthContext", "security", "completed"),
                ("5.2", "Develop real-time alerts and anomaly detection", "ai_ml", "planning"),
                ("5.3", "Build automated operational reports", "backend", "planning"),
            ]
        },
        {
            "phase_number": 6,
            "name": "Dashboard and User Interface",
            "description": "Frontend visualization and interaction",
            "status": "in_progress",
            "tasks": [
                ("6.1", "Set up Vite/React frontend foundation", "frontend", "completed"),
                ("6.2", "Implement responsive, dynamic login page", "frontend", "completed"),
                ("6.3", "Build real-time telemetry dashboard component", "frontend", "planning"),
                ("6.4", "Develop optimization results visualization", "frontend", "planning"),
            ]
        },
        {
            "phase_number": 7,
            "name": "Advanced Research Extensions",
            "description": "Future R&D",
            "status": "planning",
            "tasks": [
                ("7.1", "Incorporate ML-based predictive maintenance", "ai_ml", "planning"),
                ("7.2", "Explore multi-agent RL for dispatch", "ai_ml", "planning"),
            ]
        }
    ]

    print("Populating Phases and Tasks...")
    for pd in phases_data:
        phase, _ = Phase.objects.get_or_create(
            project=project,
            phase_number=pd["phase_number"],
            defaults={
                "name": pd["name"],
                "description": pd["description"],
                "status": pd["status"],
            }
        )

        for t_code, t_title, t_cat, t_status in pd["tasks"]:
            Task.objects.get_or_create(
                project=project,
                phase=phase,
                task_code=f"TSK-{t_code.replace('.','')}",
                defaults={
                    "title": t_title,
                    "category": t_cat,
                    "status": t_status,
                }
            )
    print("Successfully populated PM Database!")

if __name__ == "__main__":
    populate()
