export interface PhaseProgress {
  phase_number: number;
  name: string;
  status: string;
  progress: number;
}

export interface ProjectDashboard {
  project: string;
  overall_progress: number;
  total_tasks: number;
  status_breakdown: Record<string, number>;
  phases: PhaseProgress[];
  open_tech_debt: number;
  unresolved_insights: number;
}

export interface Project {
  id: number;
  name: string;
  slug: string;
  tagline: string;
  status: string;
  priority: string;
  progress_percentage: number;
  phase_count: number;
  task_count: number;
}

export interface Task {
  id: number;
  task_code: string;
  title: string;
  status: string;
  category: string;
  subtask_progress: string;
  project: number;
  phase: number;
}
