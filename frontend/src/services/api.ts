import { Customer, SupportQuery, CollaborationLog, QuerySubmitResponse } from '../types';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:5001/api';

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getCustomers(): Promise<{ customers: Customer[]; count: number }> {
    return this.request<{ customers: Customer[]; count: number }>('/customers');
  }

  async getCustomersByRegion(region: string): Promise<{ customers: Customer[]; count: number }> {
    return this.request<{ customers: Customer[]; count: number }>(`/customers?region=${region}`);
  }

  async getCustomer(customerId: string): Promise<{ customer: Customer }> {
    return this.request<{ customer: Customer }>(`/customers/${customerId}`);
  }

  async submitQuery(queryData: {
    customer_id: string;
    message: string;
    category: string;
    priority: string;
  }): Promise<QuerySubmitResponse> {
    return this.request<QuerySubmitResponse>('/support/query', {
      method: 'POST',
      body: JSON.stringify(queryData),
    });
  }

  async submitQueryStreaming(
    queryData: {
      customer_id: string;
      message: string;
      category: string;
      priority: string;
    },
    onStep: (step: any) => void,
    onComplete: (result: any) => void,
    onError: (error: string) => void
  ): Promise<void> {
    const url = `${API_BASE_URL}/support/query-stream`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        
        // Process complete lines
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep the last incomplete line in buffer
        
        for (const line of lines) {
          if (line.trim().startsWith('data: ')) {
            try {
              const data = JSON.parse(line.replace('data: ', ''));
              
              if (data.type === 'step') {
                onStep(data.step);
              } else if (data.type === 'complete') {
                onComplete(data.collaboration);
                return;
              }
            } catch (parseError) {
              console.warn('Failed to parse SSE data:', line, parseError);
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming request failed:', error);
      onError(error instanceof Error ? error.message : 'Unknown error');
    }
  }

  async getSampleQueries(): Promise<{ queries: any[] }> {
    return this.request<{ queries: any[] }>('/support/sample-queries');
  }

  async getAgentsStatus(): Promise<{
    agents: {
      us_agent: { role: string; endpoint: string; status: string; region: string };
      eu_agent: { role: string; endpoint: string; status: string; region: string };
    };
    collaboration_flow: string[];
  }> {
    return this.request('/agents/status');
  }

  async healthCheck(): Promise<{
    status: string;
    timestamp: string;
    services: { us_agent: string; eu_agent: string };
  }> {
    return this.request('/health');
  }
}

export const apiService = new ApiService();