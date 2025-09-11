export interface Customer {
  id: string;
  name: string;
  email: string;
  region: 'US' | 'EU';
  tier: 'Bronze' | 'Silver' | 'Gold' | 'Platinum';
  language: string;
  gdpr_consent: boolean;
  last_contact: string;
  preferred_channel: 'email' | 'phone' | 'chat';
  purchases: Purchase[];
}

export interface Purchase {
  id: string;
  product: string;
  amount: number;
  date: string;
  status: 'completed' | 'pending' | 'refunded';
}

export interface SupportQuery {
  id: string;
  customer_id: string;
  message: string;
  timestamp: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  category: 'billing' | 'technical' | 'general' | 'complaint';
}

export interface AgentResponse {
  agent: 'US' | 'EU';
  message: string;
  timestamp: string;
  data?: any;
}

export interface CollaborationLog {
  id: string;
  query_id: string;
  steps: AgentResponse[];
  final_response: string;
  processing_time: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface QuerySubmitResponse {
  collaboration: CollaborationLog;
  query: SupportQuery;
  customer: Customer;
}