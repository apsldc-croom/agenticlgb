import { api } from './api';

export interface PMDashboard {
    project: string;
    total_tasks: number;
    completion_percentage: number;
    by_status: Record<string, number>;
    by_priority: Record<string, number>;
    by_category: Record<string, number>;
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
    phase_name?: string;
    estimated_hours?: number;
    target_file?: string;
    tags?: PMTag[];
}

// Fallback mock implementations if the backend endpoints aren't available yet
const mockDashboard: PMDashboard = {
    project: "SLDC Grid Ops",
    total_tasks: 25,
    completion_percentage: 35,
    by_status: { completed: 8, in_progress: 5, planning: 12 },
    by_priority: { critical: 2, high: 8, medium: 10, low: 5 },
    by_category: { backend: 10, frontend: 6, ai_ml: 5, docs: 4 }
};

export const PMService = {
    getDashboard: async (): Promise<PMDashboard> => {
        try {
            const { data } = await api.get('/pm/projects/sldc-grid-ops/dashboard/');
            // Map backend fields to frontend interface
            return {
                project: data.project,
                total_tasks: data.total_tasks,
                completion_percentage: data.overall_progress,
                by_status: data.status_breakdown,
                by_priority: data.priority_breakdown || { critical: 0, high: 0, medium: 0, low: 0 },
                by_category: data.category_breakdown || { backend: 0, frontend: 0, ai_ml: 0, docs: 0 }
            };
        } catch {
            return mockDashboard;
        }
    },
    listPhases: async (): Promise<PMPhase[]> => {
        try {
            const { data } = await api.get('/pm/phases/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listFeatures: async (): Promise<PMFeature[]> => {
        try {
            const { data } = await api.get('/pm/features/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listArchLayers: async (): Promise<PMArchLayer[]> => {
        try {
            const { data } = await api.get('/pm/architecture-layers/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listDocs: async (): Promise<PMDocEntry[]> => {
        try {
            const { data } = await api.get('/pm/docs/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listTechDebt: async (): Promise<PMTechDebt[]> => {
        try {
            const { data } = await api.get('/pm/tech-debt/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listDeployments: async (): Promise<PMDeployment[]> => {
        try {
            const { data } = await api.get('/pm/deployments/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listBusinessGoals: async (): Promise<PMBusinessGoal[]> => {
        try {
            const { data } = await api.get('/pm/goals/');
            return data.results || data;
        } catch {
            return [];
        }
    },
    listTasks: async (params?: Record<string, string | number>): Promise<PMTask[]> => {
        try {
            const { data } = await api.get('/pm/tasks/', { params });
            return data.results || data;
        } catch {
            return [];
        }
    },
    updateTaskStatus: async (id: number, status: string): Promise<void> => {
        await api.patch(`/pm/tasks/${id}/`, { status });
    }
};
