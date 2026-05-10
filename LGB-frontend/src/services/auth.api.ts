import { api } from './api';

export interface TokenResponse {
  access: string;
  refresh: string;
}

export const login = async (email: string, password: string): Promise<TokenResponse> => {
  const response = await api.post<TokenResponse>('/auth/token/', { email, password });
  return response.data;
};

export const refreshToken = async (refresh: string): Promise<TokenResponse> => {
  const response = await api.post<TokenResponse>('/auth/token/refresh/', { refresh });
  return response.data;
};
