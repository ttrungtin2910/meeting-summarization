export interface AudioUploadResponse {
  task_id: string;
  message: string;
  status: string;
}

export interface TranscriptionResponse {
  task_id: string;
  transcription: string;
  transcription_language?: string;
  audio_duration?: number;
  confidence?: number;
  processed_at: string;
  audio_file_path?: string;
}

export interface MeetingSummaryResponse {
  task_id: string;
  summary: string;
  key_points: string[];
  action_items: string[];
  participants: string[];
  meeting_duration?: string;
  processed_at: string;
  audio_file_path?: string;
  transcription?: string;
  transcription_language?: string;
}

export type ProcessingStatus = 'pending' | 'uploading' | 'transcribing' | 'summarizing' | 'completed' | 'failed';

export interface ProcessingStatusResponse {
  task_id: string;
  status: ProcessingStatus;
  progress: number;
  message: string;
  result?: any;
  created_at: string;
  updated_at: string;
}