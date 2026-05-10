import { useEffect, useRef, useCallback } from 'react';
import { api } from './api';

// =========================================================
// TYPES
// =========================================================

export interface PMDashboard {
    project: string;
    total_tasks: number;
    completion_percentage: number;
    by_status: Record<string, number>;
    by_priority: Record<string, number>;
    by_category: Record<string, number>;
    overall_progress?: number;
}

export interface PMPhase {
    id: number;
    phase_number: number;
    name: string;
    description: string;
    status: string;
    duration_weeks: number;
    task_count: number;
    progress_percentage: number;
}

export interface PMFeature {
    id: number;
    name: string;
    category: string;
    status: string;
    status_display: string;
    user_facing: boolean;
}

export interface PMArchLayer {
    id: number;
    layer_number: number;
    name: string;
    directory: string;
    status: string;
}

export interface PMDocEntry {
    id: number;
    title: string;
    doc_type: string;
    doc_type_display: string;
    status: string;
    status_display: string;
    completeness: number;
}

export interface PMTechDebt {
    id: number;
    title: string;
    impact: string;
    severity: string;
    debt_type_display: string;
    affected_files: string;
}

export interface PMDeployment {
    id: number;
    environment: string;
    environment_display: string;
    status: string;
    status_display: string;
    url: string;
}

export interface PMBusinessGoal {
    id: number;
    title: string;
    goal_type_display: string;
    progress_percentage: number;
    target_metric?: string;
    current_value?: string;
    target_value?: string;
    key_results: { title: string; done: boolean }[];
}

export interface PMTag {
    id: number;
    name: string;
    color: string;
}

export interface PMTask {
    id: number;
    task_code: string;
    title: string;
    category: string;
    status: string;
    priority: string;
    phase?: number;
    phase_name?: string;
    estimated_hours?: number;
    target_file?: string;
    tags?: PMTag[];
    subtask_progress?: string;
    ai_generated?: boolean;
}

export interface PMStatusHistory {
    id: number;
    task: number;
    from_status: string;
    to_status: string;
    changed_by: number | null;
    changed_by_name: string;
    changed_at: string;
    note: string;
}

export interface PMTaskDetail extends PMTask {
    description?: string;
    milestone?: number | null;
    feature?: number | null;
    assigned_to?: number | null;
    assigned_to_name?: string | null;
    actual_hours?: number;
    ai_summary?: string;
    ai_risk_score?: number;
    due_date?: string | null;
    completed_at?: string | null;
    subtasks?: { id: number; title: string; status: string; sort_order: number }[];
    status_history?: PMStatusHistory[];
    sort_order?: number;
    created_at?: string;
    updated_at?: string;
}

export interface PMBoard {
    [status: string]: {
        label: string;
        count: number;
        tasks: PMTask[];
    };
}

export interface BulkUpdateResult {
    updated: number;
    skipped: number;
}

// =========================================================
// MOCK FALLBACK
// =========================================================

const mockDashboard: PMDashboard = {
    project: "SLDC Grid Ops",
    total_tasks: 25,
    completion_percentage: 35,
    by_status: { completed: 8, in_progress: 5, planning: 12 },
    by_priority: { critical: 2, high: 8, medium: 10, low: 5 },
    by_category: { backend: 10, frontend: 6, ai_ml: 5, docs: 4 }
};

// =========================================================
// PM SERVICE
// =========================================================

export const PMService = {

    // --- Dashboard ---
    getDashboard: async (): Promise<PMDashboard> => {
        try {
            const { data } = await api.get('/pm/projects/sldc-grid-ops/dashboard/');
            return {
                project: data.project,
                total_tasks: data.total_tasks,
                completion_percentage: data.overall_progress,
                by_status: data.status_breakdown,
                by_priority: data.priority_breakdown || {},
                by_category: data.category_breakdown || {},
            };
        } catch {
            return mockDashboard;
        }
    },

    // --- Lists ---
    listPhases: async (): Promise<PMPhase[]> => {
        try {
            const { data } = await api.get('/pm/phases/');
            return data.results ?? data;
        } catch { return []; }
    },

    listFeatures: async (): Promise<PMFeature[]> => {
        try {
            const { data } = await api.get('/pm/features/');
            return data.results ?? data;
        } catch { return []; }
    },

    listArchLayers: async (): Promise<PMArchLayer[]> => {
        try {
            const { data } = await api.get('/pm/architecture-layers/');
            return data.results ?? data;
        } catch { return []; }
    },

    listDocs: async (): Promise<PMDocEntry[]> => {
        try {
            const { data } = await api.get('/pm/docs/');
            return data.results ?? data;
        } catch { return []; }
    },

    listTechDebt: async (): Promise<PMTechDebt[]> => {
        try {
            const { data } = await api.get('/pm/tech-debt/');
            return data.results ?? data;
        } catch { return []; }
    },

    listDeployments: async (): Promise<PMDeployment[]> => {
        try {
            const { data } = await api.get('/pm/deployments/');
            return data.results ?? data;
        } catch { return []; }
    },

    listBusinessGoals: async (): Promise<PMBusinessGoal[]> => {
        try {
            const { data } = await api.get('/pm/goals/');
            return data.results ?? data;
        } catch { return []; }
    },

    listTasks: async (params?: Record<string, string | number>): Promise<PMTask[]> => {
        try {
            const { data } = await api.get('/pm/tasks/', { params });
            return data.results ?? data;
        } catch { return []; }
    },

    // --- Task detail ---
    getTask: async (id: number): Promise<PMTaskDetail | null> => {
        try {
            const { data } = await api.get(`/pm/tasks/${id}/`);
            return data;
        } catch { return null; }
    },

    // --- Board (Kanban grouped by status) ---
    getBoard: async (projectId?: number): Promise<PMBoard> => {
        try {
            const params = projectId ? { project: projectId } : {};
            const { data } = await api.get('/pm/tasks/board/', { params });
            return data;
        } catch { return {}; }
    },

    // --- Status updates ---
    updateTaskStatus: async (id: number, newStatus: string): Promise<PMTask | null> => {
        try {
            const { data } = await api.patch(`/pm/tasks/${id}/`, { status: newStatus });
            return data;
        } catch { return null; }
    },

    completeTask: async (id: number): Promise<PMTaskDetail | null> => {
        try {
            const { data } = await api.post(`/pm/tasks/${id}/complete/`);
            return data;
        } catch { return null; }
    },

    bulkUpdateStatus: async (ids: number[], newStatus: string): Promise<BulkUpdateResult> => {
        const { data } = await api.post('/pm/tasks/bulk-update/', {
            ids,
            status: newStatus,
        });
        return data;
    },

    // --- History ---
    getTaskHistory: async (id: number): Promise<PMStatusHistory[]> => {
        try {
            const { data } = await api.get(`/pm/tasks/${id}/history/`);
            return data;
        } catch { return []; }
    },
};

// =========================================================
// POLLING HOOK — 30s auto-refresh
// =========================================================

/**
 * usePMPolling
 * Calls `fetchFn` immediately, then every `intervalMs` (default 30s).
 * Stops polling when the component unmounts.
 *
 * Usage:
 *   usePMPolling(fetchTasks);
 *   usePMPolling(fetchDashboard, 15_000);
 */
export function usePMPolling(
    fetchFn: () => Promise<void>,
    intervalMs = 30_000
) {
    const savedFn = useRef(fetchFn);

    useEffect(() => {
        savedFn.current = fetchFn;
    }, [fetchFn]);

    const tick = useCallback(() => {
        savedFn.current();
    }, []);

    useEffect(() => {
        tick(); // immediate first call
        const id = setInterval(tick, intervalMs);
        return () => clearInterval(id);
    }, [tick, intervalMs]);
}

