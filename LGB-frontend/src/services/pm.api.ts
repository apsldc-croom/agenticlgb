import { api } from './api';
import type { ProjectDashboard, Project, Task } from '../modules/pm/types';

export const pmApi = {
  getProjects: async (): Promise<Project[]> => {
    const { data } = await api.get('/pm/projects/');
    return data.results || data;
  },
  getProjectDashboard: async (slug: string): Promise<ProjectDashboard> => {
    const { data } = await api.get(`/pm/projects/${slug}/dashboard/`);
    return data;
  },
  getTasks: async (params?: Record<string, any>): Promise<Task[]> => {
    const { data } = await api.get('/pm/tasks/', { params });
    return data.results || data;
  },
};
