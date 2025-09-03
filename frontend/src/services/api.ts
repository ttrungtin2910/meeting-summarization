import axios from 'axios';
import {
  AudioUploadResponse,
  MeetingSummaryResponse,
  ProcessingStatusResponse,
  TranscriptionResponse,
} from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for large file uploads
});

// Request interceptor for adding auth headers if needed
api.interceptors.request.use(
  (config) => {
    // Add auth token here if needed
    // config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const audioAPI = {
  // Upload audio file and get complete summary (synchronous)
  async processAudioComplete(file: File): Promise<MeetingSummaryResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<MeetingSummaryResponse>(
      '/api/v1/process-audio',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    
    return response.data;
  },

  // Upload audio file for async processing
  async uploadAudio(file: File): Promise<AudioUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<AudioUploadResponse>(
      '/api/v1/upload-audio',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    
    return response.data;
  },

  // Get task processing status
  async getTaskStatus(taskId: string): Promise<ProcessingStatusResponse> {
    const response = await api.get<ProcessingStatusResponse>(
      `/api/v1/tasks/${taskId}/status`
    );
    return response.data;
  },

  // Get transcription result
  async getTranscription(taskId: string): Promise<TranscriptionResponse> {
    const response = await api.get<TranscriptionResponse>(
      `/api/v1/tasks/${taskId}/transcription`
    );
    return response.data;
  },

  // Get meeting summary
  async getMeetingSummary(taskId: string): Promise<MeetingSummaryResponse> {
    const response = await api.get<MeetingSummaryResponse>(
      `/api/v1/tasks/${taskId}/summary`
    );
    return response.data;
  },

  // Transcription-only endpoints
  async transcribeAudio(file: File): Promise<TranscriptionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<TranscriptionResponse>('/api/transcription/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async createSummaryFromTranscription(taskId: string): Promise<MeetingSummaryResponse> {
    const response = await api.post<MeetingSummaryResponse>(`/api/transcription/summarize/${taskId}`);
    return response.data;
  },
};

export default api;
