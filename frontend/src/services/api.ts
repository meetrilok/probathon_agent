import axios from 'axios';
import type { DashboardResponse, RequiredInputsResponse, UseCasePayload, ValidationPayload } from '../types/api';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api',
});

export const fetchRequiredInputs = async (): Promise<RequiredInputsResponse> => {
  const response = await client.get('/required-inputs');
  return response.data;
};

export const ingestUseCase = async (payload: UseCasePayload): Promise<void> => {
  await client.post('/use-cases', payload);
};

export const validateIdea = async (payload: ValidationPayload): Promise<any> => {
  const response = await client.post('/validate', payload);
  return response.data;
};

export const fetchDashboard = async (): Promise<DashboardResponse> => {
  const response = await client.get('/dashboard');
  return response.data;
};
