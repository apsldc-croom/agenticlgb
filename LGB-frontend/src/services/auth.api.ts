import { api } from './api';

export interface TokenResponse {
  access: string;
  refresh: string;
}

export const login = async (username: string, password: string): Promise<TokenResponse> => {
  const response = await api.post<TokenResponse>('/auth/token/', { username, password });
  return response.data;
};

export const refreshToken = async (refresh: string): Promise<TokenResponse> => {
  const response = await api.post<TokenResponse>('/auth/token/refresh/', { refresh });
  return response.data;
};
