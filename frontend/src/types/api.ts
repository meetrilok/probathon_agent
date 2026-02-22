export interface InputDescriptor {
  key: string;
  label: string;
  required: boolean;
  description: string;
}

export interface RequiredInputsResponse {
  ingestion: InputDescriptor[];
  validation: InputDescriptor[];
  infrastructure: InputDescriptor[];
}

export interface UseCasePayload {
  title: string;
  description: string;
  lob: string;
  contact_email?: string;
  source_type: string;
  source_uri?: string;
}

export interface ValidationPayload {
  idea_title: string;
  idea_description: string;
  lob: string;
}

export interface DashboardResponse {
  total_use_cases: number;
  by_lob: Record<string, number>;
  recent_use_cases: Array<{ id: number; title: string; lob: string; created_at: string }>;
}
