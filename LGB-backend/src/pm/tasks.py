"""
pm/tasks.py

Celery tasks for the PM module.
Background jobs for reporting, notifications, and AI ops.
"""

import logging

logger = logging.getLogger(__name__)

# Celery app import is deferred to avoid import-time issues
# when Celery is not configured. Uncomment when Celery is set up:
#
# from worker.celery import app
#
# @app.task(bind=True, name="pm.generate_project_report")
# def generate_project_report(self, project_id: int):
#     """Generate a comprehensive project status report."""
#     from .selectors import get_project_summary
#     summary = get_project_summary(project_id)
#     logger.info("Generated report for project %s: %s", project_id, summary)
#     return summary
#
#
# @app.task(bind=True, name="pm.check_overdue_tasks")
# def check_overdue_tasks(self):
#     """Periodic task: find and log overdue tasks."""
#     from .selectors import get_overdue_tasks
#     overdue = get_overdue_tasks()
#     logger.warning("Found %d overdue tasks.", len(overdue))
#     return overdue
#
#
# @app.task(bind=True, name="pm.sync_ai_insights")
# def sync_ai_insights(self, project_id: int):
#     """Generate AI insights for a project (calls AI subsystem)."""
#     logger.info("AI insight sync requested for project %s.", project_id)
#     # TODO: Integrate with ai/ subsystem
#     pass
