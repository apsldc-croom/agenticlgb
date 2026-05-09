#!/bin/bash
# ============================================================
# LGB Scaffold — Part 1/4
# Docs, Coding Standards, Project Management, Docker, CI/CD, Root Configs
# ============================================================
set -e
ROOT="."

# --- .github/workflows ---
mkdir -p "$ROOT/.github/workflows"
echo "# CI: Lint + Test on PR" > "$ROOT/.github/workflows/ci.yml"
echo "# CD: Auto-deploy to staging" > "$ROOT/.github/workflows/cd-staging.yml"
echo "# CD: Tag-triggered production deploy" > "$ROOT/.github/workflows/cd-production.yml"

# --- docker/ ---
mkdir -p "$ROOT/docker/nginx/conf.d"
mkdir -p "$ROOT/docker/monitoring/prometheus"
mkdir -p "$ROOT/docker/monitoring/grafana/provisioning/dashboards"
mkdir -p "$ROOT/docker/monitoring/grafana/provisioning/datasources"

echo "# Django multi-stage Dockerfile" > "$ROOT/docker/Dockerfile.backend"
echo "# Vite production Dockerfile" > "$ROOT/docker/Dockerfile.frontend"
echo "# Celery worker Dockerfile" > "$ROOT/docker/Dockerfile.worker"
echo "# Daphne ASGI Dockerfile [P3]" > "$ROOT/docker/Dockerfile.channels"
echo "# Main Nginx configuration" > "$ROOT/docker/nginx/nginx.conf"
echo "# Backend upstream config" > "$ROOT/docker/nginx/conf.d/upstream.conf"
echo "# SSL/TLS configuration" > "$ROOT/docker/nginx/conf.d/ssl.conf"
echo "# Full stack docker-compose" > "$ROOT/docker/docker-compose.yml"
echo "# Prometheus scrape config [P7]" > "$ROOT/docker/monitoring/prometheus/prometheus.yml"
echo "# Grafana settings [P7]" > "$ROOT/docker/monitoring/grafana/grafana.ini"
echo "{}" > "$ROOT/docker/monitoring/grafana/provisioning/dashboards/LGB.json"
echo "# Prometheus datasource [P7]" > "$ROOT/docker/monitoring/grafana/provisioning/datasources/prometheus.yml"
echo "# Monitoring stack compose [P7]" > "$ROOT/docker/monitoring/docker-compose.monitoring.yml"

# --- Root compose and env files ---
[ -f "$ROOT/docker-compose.yml" ] || echo "# Dev docker-compose [P1]" > "$ROOT/docker-compose.yml"
echo "# Production docker-compose [P1]" > "$ROOT/docker-compose.prod.yml"
echo "# === LGB Environment Template ===" > "$ROOT/.env.example"
echo "# Dev environment [P1]" > "$ROOT/.env.dev"
echo "# Staging environment [P1]" > "$ROOT/.env.staging"
echo "# Production environment [P1] — secrets via vault" > "$ROOT/.env.prod"

# --- docs/ ---
mkdir -p "$ROOT/docs/requirements"
mkdir -p "$ROOT/docs/api"
mkdir -p "$ROOT/docs/database"
mkdir -p "$ROOT/docs/workflows"
mkdir -p "$ROOT/docs/decisions"
mkdir -p "$ROOT/docs/runbooks"

echo "# LGB Platform Overview" > "$ROOT/docs/overview.md"
echo "# 26-Layer Architecture Reference" > "$ROOT/docs/architecture.md"
echo "# Phased Execution Roadmap" > "$ROOT/docs/roadmap.md"
echo "# Functional Requirements" > "$ROOT/docs/requirements/functional.md"
echo "# Non-Functional Requirements" > "$ROOT/docs/requirements/non-functional.md"
echo "# API v1 Contract Documentation" > "$ROOT/docs/api/v1.md"
echo "# Database Schema & ERD" > "$ROOT/docs/database/schema.md"
echo "# Authentication Flow" > "$ROOT/docs/workflows/auth-flow.md"
cat > "$ROOT/docs/decisions/adr-template.md" << 'EOF'
# ADR-XXX: Title

## Status
Proposed

## Context
## Decision
## Consequences
EOF
echo "# ADR-001: Monorepo Structure" > "$ROOT/docs/decisions/adr-001-monorepo.md"
echo "# ADR-002: Django + DRF Stack" > "$ROOT/docs/decisions/adr-002-django-drf.md"
echo "# Deployment Runbook" > "$ROOT/docs/runbooks/deployment.md"
echo "# Incident Response Playbook" > "$ROOT/docs/runbooks/incident-response.md"

# --- coding/ ---
mkdir -p "$ROOT/coding"
echo "# Code Formatting Standards" > "$ROOT/coding/formatting.md"
echo "# Testing Conventions" > "$ROOT/coding/testing.md"
echo "# Anti-Patterns to Avoid" > "$ROOT/coding/anti-patterns.md"
echo "# AI-Assisted Development Rules" > "$ROOT/coding/ai-prompting.md"
echo "# Git Commit Conventions" > "$ROOT/coding/commit-conventions.md"

# --- project_management/ ---
mkdir -p "$ROOT/project_management/phases"
mkdir -p "$ROOT/project_management/tasks"

echo "# Phase 1: Problem Formalisation" > "$ROOT/project_management/phases/phase1-formalisation.md"
echo "# Phase 2: Data Infrastructure" > "$ROOT/project_management/phases/phase2-data.md"
echo "# Phase 3: Optimisation Engine" > "$ROOT/project_management/phases/phase3-optimisation.md"
echo "# Phase 4: Scenario Engine" > "$ROOT/project_management/phases/phase4-scenario.md"
echo "# Phase 5: Operational Intelligence Layer" > "$ROOT/project_management/phases/phase5-intelligence.md"
echo "# Phase 6: Dashboard and User Interface" > "$ROOT/project_management/phases/phase6-dashboard.md"
echo "# Phase 7: Advanced Research Extensions" > "$ROOT/project_management/phases/phase7-advanced.md"
echo "# Task Backlog" > "$ROOT/project_management/tasks/backlog.md"
echo "# Project Milestones" > "$ROOT/project_management/milestones.md"

echo "✅ Part 1 scaffolding complete: docs, coding, project_management, docker, .github, root configs"
#!/bin/bash
# ============================================================
# LGB Scaffold — Part 2/4
# AI Subsystem: providers, prompts, services, RAG, agents, graph, evaluation
# ============================================================
set -e
AI="LGB-backend/src/ai"

py() { [ -f "$1" ] || echo "\"\"\"$(basename "$1" .py) module — $2\"\"\"" > "$1"; }
init() { [ -f "$1/__init__.py" ] || touch "$1/__init__.py"; }

# --- ai/ root ---
mkdir -p "$AI"
init "$AI"
py "$AI/config.py" "AI settings: model names, API keys, defaults"
py "$AI/client.py" "Provider-agnostic LLM client factory"
py "$AI/tasks.py" "Celery tasks for async AI jobs"

# --- ai/providers/ [P4] ---
mkdir -p "$AI/providers"
init "$AI/providers"
py "$AI/providers/base.py" "Abstract LLM provider: generate(), embed(), stream()"
py "$AI/providers/openai.py" "OpenAI GPT-4o / embeddings provider"
py "$AI/providers/anthropic.py" "Anthropic Claude provider (future)"
py "$AI/providers/local.py" "Ollama / vLLM local model provider (future)"

# --- ai/prompts/ [P4] ---
mkdir -p "$AI/prompts/templates/system"
mkdir -p "$AI/prompts/templates/rag"
mkdir -p "$AI/prompts/templates/agent"
init "$AI/prompts"
py "$AI/prompts/registry.py" "Central prompt registry with versioning"
py "$AI/prompts/builder.py" "Dynamic prompt construction with context injection"
py "$AI/prompts/versioning.py" "Prompt version tracking and A/B testing"
echo "# Platform assistant system prompt" > "$AI/prompts/templates/system/assistant.yaml"
echo "# Content moderation system prompt" > "$AI/prompts/templates/system/moderator.yaml"
echo "# RAG retrieval prompt template" > "$AI/prompts/templates/rag/retrieval.yaml"
echo "# RAG answer synthesis prompt" > "$AI/prompts/templates/rag/synthesis.yaml"
echo "# Agent planning prompt" > "$AI/prompts/templates/agent/planner.yaml"
echo "# Agent execution prompt" > "$AI/prompts/templates/agent/executor.yaml"

# --- ai/services/ [P4] ---
mkdir -p "$AI/services"
init "$AI/services"
py "$AI/services/summarizer.py" "Thread/forum content summarization"
py "$AI/services/recommender.py" "Content and connection recommendations"
py "$AI/services/moderator.py" "AI-assisted content moderation"
py "$AI/services/classifier.py" "Topic/intent classification"
py "$AI/services/search.py" "Semantic search service"

# --- ai/api/ [P4] ---
mkdir -p "$AI/api"
init "$AI/api"
py "$AI/api/urls.py" "AI endpoint URL routing"
py "$AI/api/views.py" "AI feature API views"
py "$AI/api/serializers.py" "AI request/response schemas"

# --- ai/rag/ [P5] ---
mkdir -p "$AI/rag/loaders"
mkdir -p "$AI/rag/chunkers"
mkdir -p "$AI/rag/embedders"
mkdir -p "$AI/rag/stores"
mkdir -p "$AI/rag/retrievers"
mkdir -p "$AI/rag/context"
init "$AI/rag"
py "$AI/rag/pipeline.py" "RAG orchestrator: query -> retrieve -> generate"
init "$AI/rag/loaders"
py "$AI/rag/loaders/base.py" "Abstract document loader"
py "$AI/rag/loaders/markdown.py" "Markdown file loader"
py "$AI/rag/loaders/pdf.py" "PDF document extraction"
py "$AI/rag/loaders/html.py" "Web page / HTML loader"
py "$AI/rag/loaders/code.py" "Source code loader (Python, JS, etc.)"
py "$AI/rag/loaders/database.py" "Django model content loader (threads, forums)"
init "$AI/rag/chunkers"
py "$AI/rag/chunkers/base.py" "Abstract text chunker"
py "$AI/rag/chunkers/recursive.py" "Recursive character text splitter"
py "$AI/rag/chunkers/semantic.py" "Embedding-based semantic chunking"
py "$AI/rag/chunkers/code.py" "AST-aware code chunking"
init "$AI/rag/embedders"
py "$AI/rag/embedders/base.py" "Abstract embedder interface"
py "$AI/rag/embedders/openai.py" "OpenAI text-embedding-3 embedder"
py "$AI/rag/embedders/local.py" "Sentence-transformers local embedder (future)"
init "$AI/rag/stores"
py "$AI/rag/stores/base.py" "Abstract vector store interface"
py "$AI/rag/stores/pgvector.py" "PostgreSQL pgvector backend (default)"
py "$AI/rag/stores/qdrant.py" "Qdrant vector store adapter (future)"
py "$AI/rag/stores/pinecone.py" "Pinecone vector store adapter (future)"
init "$AI/rag/retrievers"
py "$AI/rag/retrievers/base.py" "Abstract retriever interface"
py "$AI/rag/retrievers/dense.py" "Dense vector similarity search"
py "$AI/rag/retrievers/hybrid.py" "Dense + keyword hybrid search"
py "$AI/rag/retrievers/reranker.py" "Cross-encoder reranking"
py "$AI/rag/retrievers/contextual.py" "Context-aware retrieval with metadata filtering"
init "$AI/rag/context"
py "$AI/rag/context/builder.py" "Context window assembly from retrieved chunks"
py "$AI/rag/context/compressor.py" "Context compression to fit token limits"
py "$AI/rag/context/ranker.py" "Rank and deduplicate context chunks"

# --- ai/ingestion/ [P5] ---
mkdir -p "$AI/ingestion/sources"
mkdir -p "$AI/ingestion/processors"
init "$AI/ingestion"
py "$AI/ingestion/pipeline.py" "Content ingestion orchestrator"
init "$AI/ingestion/sources"
py "$AI/ingestion/sources/docs.py" "Ingest from docs/ directory"
py "$AI/ingestion/sources/codebase.py" "Ingest repository source code"
py "$AI/ingestion/sources/telemetry.py" "Ingest historical telemetry and market data"
py "$AI/ingestion/sources/external.py" "Ingest external URLs/APIs"
init "$AI/ingestion/processors"
py "$AI/ingestion/processors/cleaner.py" "Text cleaning and normalization"
py "$AI/ingestion/processors/metadata.py" "Metadata extraction and attachment"
py "$AI/ingestion/processors/deduplicator.py" "Content deduplication"
py "$AI/ingestion/tasks.py" "Celery tasks for background ingestion"

# --- ai/search/ [P5] ---
mkdir -p "$AI/search"
init "$AI/search"
py "$AI/search/engine.py" "Search orchestrator (vector + keyword)"
py "$AI/search/indexer.py" "Index manager for all content types"
py "$AI/search/filters.py" "Search filters (date, type, author, group)"
py "$AI/search/tasks.py" "Background reindexing tasks"

# --- ai/agent/ [P6] ---
mkdir -p "$AI/agent/planners"
mkdir -p "$AI/agent/executors"
mkdir -p "$AI/agent/tools"
mkdir -p "$AI/agent/memory"
mkdir -p "$AI/agent/agents"
init "$AI/agent"
py "$AI/agent/base.py" "Abstract agent: plan -> execute -> reflect"
init "$AI/agent/planners"
py "$AI/agent/planners/base.py" "Abstract planner interface"
py "$AI/agent/planners/react.py" "ReAct (Reason + Act) planner"
py "$AI/agent/planners/tree_of_thought.py" "Tree-of-thought planner"
init "$AI/agent/executors"
py "$AI/agent/executors/base.py" "Abstract executor interface"
py "$AI/agent/executors/sequential.py" "Sequential step executor"
py "$AI/agent/executors/parallel.py" "Parallel step executor"
init "$AI/agent/tools"
py "$AI/agent/tools/registry.py" "Tool registry and discovery"
py "$AI/agent/tools/base.py" "Abstract tool interface"
py "$AI/agent/tools/search.py" "Search platform content tool"
py "$AI/agent/tools/database.py" "Query database tool"
py "$AI/agent/tools/user_lookup.py" "Look up user profiles tool"
py "$AI/agent/tools/summarize.py" "Summarize content tool"
py "$AI/agent/tools/notify.py" "Send notification tool"
py "$AI/agent/tools/web.py" "Web search / URL fetch tool"
init "$AI/agent/memory"
py "$AI/agent/memory/base.py" "Abstract memory interface"
py "$AI/agent/memory/short_term.py" "Conversation buffer (in-context)"
py "$AI/agent/memory/long_term.py" "Persistent memory (vector DB backed)"
py "$AI/agent/memory/episodic.py" "Past interaction recall"
py "$AI/agent/memory/working.py" "Current task scratchpad"
init "$AI/agent/agents"
py "$AI/agent/agents/assistant.py" "Platform assistant (user-facing)"
py "$AI/agent/agents/moderator.py" "Content moderation agent"
py "$AI/agent/agents/researcher.py" "Research and summarization agent"
py "$AI/agent/agents/engineer.py" "Internal engineering assistant"

# --- ai/graph/ [P6] ---
mkdir -p "$AI/graph/storage"
init "$AI/graph"
py "$AI/graph/builder.py" "Build knowledge graph from platform data"
py "$AI/graph/models.py" "Node, Edge, KnowledgeTriple models"
py "$AI/graph/query.py" "Graph traversal and querying"
py "$AI/graph/enricher.py" "AI-powered entity/relation extraction"
init "$AI/graph/storage"
py "$AI/graph/storage/base.py" "Abstract graph store interface"
py "$AI/graph/storage/postgres.py" "PostgreSQL adjacency list (default)"
py "$AI/graph/storage/neo4j.py" "Neo4j adapter (future)"
py "$AI/graph/tasks.py" "Background graph building tasks"

# --- ai/evaluation/ [P6] ---
mkdir -p "$AI/evaluation/metrics"
mkdir -p "$AI/evaluation/datasets"
mkdir -p "$AI/evaluation/reports"
init "$AI/evaluation"
py "$AI/evaluation/runner.py" "Evaluation test runner"
init "$AI/evaluation/metrics"
py "$AI/evaluation/metrics/relevance.py" "Answer relevance scoring"
py "$AI/evaluation/metrics/faithfulness.py" "Hallucination detection"
py "$AI/evaluation/metrics/retrieval.py" "Retrieval precision/recall"
py "$AI/evaluation/metrics/latency.py" "Response time metrics"
echo '[]' > "$AI/evaluation/datasets/golden_qa.json"
touch "$AI/evaluation/reports/.gitkeep"

# --- ai/orchestration/ [P6] ---
mkdir -p "$AI/orchestration"
init "$AI/orchestration"
py "$AI/orchestration/router.py" "Route queries to appropriate agent"
py "$AI/orchestration/chain.py" "Chain multiple AI steps"
py "$AI/orchestration/supervisor.py" "Multi-agent supervisor pattern"

echo "✅ Part 2 scaffolding complete: ai/ subsystem (providers, prompts, RAG, agents, graph, evaluation)"
#!/bin/bash
# ============================================================
# LGB Scaffold — Part 3/4
# Backend: core/, worker/, observability/, analytics/, security/,
#          features/, search/, cache/, events_bus/, gateway/, tests/
# ============================================================
set -e
BE="LGB-backend/src"

py() { mkdir -p "$(dirname "$1")"; [ -f "$1" ] || echo "\"\"\"$(basename "$1" .py) module — $2\"\"\"" > "$1"; }
init() { [ -f "$1/__init__.py" ] || touch "$1/__init__.py"; }

# --- core/ expansions [P2] ---
mkdir -p "$BE/core/middleware"
mkdir -p "$BE/core/utils"
mkdir -p "$BE/core/db"
init "$BE/core/middleware"
init "$BE/core/utils"
init "$BE/core/db"
[ -f "$BE/core/serializers.py" ] || py "$BE/core/serializers.py" "Base serializer mixins"
[ -f "$BE/core/permissions.py" ] || py "$BE/core/permissions.py" "Shared permission classes"
py "$BE/core/pagination.py" "Standard pagination classes"
py "$BE/core/throttling.py" "Rate limiting configuration"
py "$BE/core/exceptions.py" "Custom DRF exception handler"
py "$BE/core/middleware/request_id.py" "Attach UUID to every request"
py "$BE/core/middleware/timing.py" "Request duration logging"
py "$BE/core/middleware/security.py" "Security headers middleware"
py "$BE/core/utils/email.py" "Email sending utility"
py "$BE/core/utils/storage.py" "S3-compatible file storage helper"
py "$BE/core/utils/validators.py" "Shared input validators"
py "$BE/core/db/routers.py" "DB router for read replicas [P9]"
py "$BE/core/db/indexes.py" "Custom composite index definitions [P9]"
py "$BE/core/db/profiler.py" "Query count/time profiler middleware [P9]"

# --- config/ additions [P1] ---
[ -f "$BE/config/settings/staging.py" ] || py "$BE/config/settings/staging.py" "Staging environment settings"
[ -f "$BE/config/settings/production.py" ] || py "$BE/config/settings/production.py" "Production environment settings"
[ -f "$BE/config/routing.py" ] || py "$BE/config/routing.py" "Django Channels WebSocket routing [P3]"

# --- worker/ [P2] ---
mkdir -p "$BE/worker"
init "$BE/worker"
py "$BE/worker/celery.py" "Celery app factory and configuration"
py "$BE/worker/schedules.py" "Periodic task schedule (celery beat)"
py "$BE/worker/health.py" "Worker health check endpoint"

# --- Domain app enhancements [P2] — add services/selectors/tasks/tests ---
for app in forecasting generators scheduling market network scenarios intelligence telemetry; do
    APP="$BE/apps/$app"
    [ -f "$APP/services.py" ] || py "$APP/services.py" "Business logic layer for $app"
    [ -f "$APP/selectors.py" ] || py "$APP/selectors.py" "Query/read logic layer for $app"
    [ -f "$APP/tasks.py" ] || py "$APP/tasks.py" "Celery background tasks for $app"
    mkdir -p "$APP/tests"
    init "$APP/tests"
    [ -f "$APP/tests/test_models.py" ] || py "$APP/tests/test_models.py" "Model unit tests for $app"
    [ -f "$APP/tests/test_services.py" ] || py "$APP/tests/test_services.py" "Service layer tests for $app"
    [ -f "$APP/tests/test_api.py" ] || py "$APP/tests/test_api.py" "API integration tests for $app"
done

# --- websockets/ enhancements [P3] ---
STREAMS="$BE/apps/telemetry"
[ -f "$STREAMS/consumers.py" ] || py "$STREAMS/consumers.py" "Django Channels WebSocket consumers for live telemetry"
[ -f "$STREAMS/routing.py" ] || py "$STREAMS/routing.py" "WebSocket URL routing"

# --- observability/ [P7] ---
mkdir -p "$BE/observability/logging"
mkdir -p "$BE/observability/metrics"
mkdir -p "$BE/observability/tracing"
mkdir -p "$BE/observability/health"
init "$BE/observability"
init "$BE/observability/logging"
py "$BE/observability/logging/config.py" "Structured JSON logging configuration"
py "$BE/observability/logging/formatters.py" "Custom log formatters (JSON, human)"
py "$BE/observability/logging/filters.py" "PII scrubbing, log level filtering"
py "$BE/observability/logging/handlers.py" "File, stdout, external handlers"
init "$BE/observability/metrics"
py "$BE/observability/metrics/collectors.py" "Request count, latency, error rate"
py "$BE/observability/metrics/exporters.py" "Prometheus endpoint exporter"
py "$BE/observability/metrics/business.py" "Business metrics (signups, posts, DAU)"
py "$BE/observability/metrics/middleware.py" "Auto-collect per-request metrics"
init "$BE/observability/tracing"
py "$BE/observability/tracing/config.py" "OpenTelemetry SDK setup"
py "$BE/observability/tracing/sampler.py" "Trace sampling strategy"
py "$BE/observability/tracing/middleware.py" "Auto-trace requests and DB queries"
init "$BE/observability/health"
py "$BE/observability/health/checks.py" "Custom health check logic (DB, Redis, AI)"
py "$BE/observability/health/urls.py" "Health check endpoints"

# --- analytics/ [P7] ---
mkdir -p "$BE/analytics/aggregators"
mkdir -p "$BE/analytics/storage"
init "$BE/analytics"
py "$BE/analytics/engine.py" "Data processing orchestrator"
py "$BE/analytics/aggregators/daily.py" "Daily metric aggregation"
py "$BE/analytics/tasks.py" "Background analytics processing"

echo "✅ Part 3 scaffolding complete: backend core, observability, analytics"