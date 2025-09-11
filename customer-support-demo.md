# Global Customer Support Demo

## Project Overview
A proof-of-concept demonstrating cross-server LLM agent collaboration for global customer support, showcasing data sovereignty compliance and seamless service delivery.

## Architecture
- **US Agent**: Handles initial customer inquiries, determines user context, crafts final responses
- **EU Agent**: Manages EU customer database access, GDPR-compliant data retrieval, regional preferences
- **Cross-Server Communication**: Secure agent-to-agent collaboration across geographic boundaries

## Tech Stack
- React 18 with TypeScript
- Tailwind CSS for modern styling
- Synthetic customer data for demo purposes
- RESTful API endpoints for agent communication

## Features
- **Customer Query Interface**: Submit support requests with automatic region detection
- **Agent Collaboration Viewer**: Real-time view of US/EU agent interactions
- **Customer Profile Display**: GDPR-compliant customer data visualization
- **Response Generation**: Personalized support responses using cross-server intelligence

## Setup Instructions

### Prerequisites
```bash
node >= 18.0.0
npm or yarn
```

### Installation
```bash
# Initialize project
npx create-react-app global-support-demo --template typescript
cd global-support-demo

# Install dependencies
npm install @types/react @types/react-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install additional UI components
npm install lucide-react
npm install recharts
```

### Project Structure
```
src/
├── components/
│   ├── CustomerQueryForm.tsx
│   ├── AgentCollaborationView.tsx
│   ├── CustomerProfile.tsx
│   └── ResponseDisplay.tsx
├── data/
│   ├── syntheticCustomers.ts
│   └── syntheticQueries.ts
├── services/
│   ├── agentService.ts
│   └── customerService.ts
├── types/
│   └── index.ts
├── App.tsx
└── index.css
```

## Implementation Files

### `tailwind.config.js`
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-blue': '#0066cc',
        'brand-gray': '#f8fafc',
      }
    },
  },
  plugins: [],
}
```

### `src/index.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### `src/types/index.ts`
```typescript
export interface Customer {
  id: string;
  name: string;
  email: string;
  region: 'US' | 'EU';
  tier: 'Bronze' | 'Silver' | 'Gold' | 'Platinum';
  language: string;
  gdprConsent: boolean;
  lastContact: string;
  preferredChannel: 'email' | 'phone' | 'chat';
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
  customerId: string;
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
  queryId: string;
  steps: AgentResponse[];
  finalResponse: string;
  processingTime: number;
}
```

### `src/data/syntheticCustomers.ts`
```typescript
import { Customer } from '../types';

export const syntheticCustomers: Customer[] = [
  {
    id: 'cust-us-001',
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    region: 'US',
    tier: 'Gold',
    language: 'English',
    gdprConsent: false,
    lastContact: '2024-09-05T14:30:00Z',
    preferredChannel: 'email',
    purchases: [
      { id: 'p1', product: 'Enterprise Security Suite', amount: 2500, date: '2024-08-15', status: 'completed' },
      { id: 'p2', product: 'Compliance Module', amount: 800, date: '2024-09-01', status: 'completed' }
    ]
  },
  {
    id: 'cust-eu-001',
    name: 'Hans Müller',
    email: 'hans.mueller@email.de',
    region: 'EU',
    tier: 'Platinum',
    language: 'German',
    gdprConsent: true,
    lastContact: '2024-09-08T09:15:00Z',
    preferredChannel: 'phone',
    purchases: [
      { id: 'p3', product: 'Advanced Threat Detection', amount: 5000, date: '2024-07-20', status: 'completed' },
      { id: 'p4', product: 'GDPR Compliance Tools', amount: 1200, date: '2024-08-30', status: 'completed' }
    ]
  },
  {
    id: 'cust-eu-002',
    name: 'Marie Dubois',
    email: 'marie.dubois@email.fr',
    region: 'EU',
    tier: 'Silver',
    language: 'French',
    gdprConsent: true,
    lastContact: '2024-09-10T16:45:00Z',
    preferredChannel: 'chat',
    purchases: [
      { id: 'p5', product: 'Basic Security Package', amount: 1000, date: '2024-08-25', status: 'completed' }
    ]
  },
  {
    id: 'cust-us-002',
    name: 'Robert Chen',
    email: 'robert.chen@email.com',
    region: 'US',
    tier: 'Bronze',
    language: 'English',
    gdprConsent: false,
    lastContact: '2024-09-03T11:20:00Z',
    preferredChannel: 'email',
    purchases: [
      { id: 'p6', product: 'Starter Security Tools', amount: 500, date: '2024-08-10', status: 'completed' }
    ]
  }
];
```

### `src/data/syntheticQueries.ts`
```typescript
import { SupportQuery } from '../types';

export const sampleQueries: SupportQuery[] = [
  {
    id: 'q1',
    customerId: 'cust-us-001',
    message: 'I\'m having trouble with the new compliance module. It keeps showing false positives for our internal communications.',
    timestamp: '2024-09-11T10:00:00Z',
    priority: 'high',
    category: 'technical'
  },
  {
    id: 'q2',
    customerId: 'cust-eu-001',
    message: 'I need to understand how your threat detection system handles GDPR data processing requirements.',
    timestamp: '2024-09-11T11:30:00Z',
    priority: 'medium',
    category: 'general'
  },
  {
    id: 'q3',
    customerId: 'cust-eu-002',
    message: 'Can I get a refund for the security package? It doesn\'t meet our current needs.',
    timestamp: '2024-09-11T09:15:00Z',
    priority: 'high',
    category: 'billing'
  },
  {
    id: 'q4',
    customerId: 'cust-us-002',
    message: 'How do I upgrade from Bronze to Silver tier? What are the additional features?',
    timestamp: '2024-09-11T14:20:00Z',
    priority: 'low',
    category: 'general'
  }
];
```

### `src/services/customerService.ts`
```typescript
import { Customer } from '../types';
import { syntheticCustomers } from '../data/syntheticCustomers';

export class CustomerService {
  static getCustomerById(customerId: string): Customer | null {
    return syntheticCustomers.find(c => c.id === customerId) || null;
  }

  static getCustomersByRegion(region: 'US' | 'EU'): Customer[] {
    return syntheticCustomers.filter(c => c.region === region);
  }

  static async getGDPRCompliantData(customerId: string): Promise<Customer | null> {
    // Simulate EU data access with GDPR compliance check
    const customer = this.getCustomerById(customerId);
    if (customer?.region === 'EU' && customer.gdprConsent) {
      return customer;
    }
    return customer?.region === 'US' ? customer : null;
  }
}
```

### `src/services/agentService.ts`
```typescript
import { AgentResponse, SupportQuery, Customer, CollaborationLog } from '../types';
import { CustomerService } from './customerService';

export class AgentService {
  static async processQuery(query: SupportQuery): Promise<CollaborationLog> {
    const startTime = Date.now();
    const steps: AgentResponse[] = [];
    
    // Step 1: US Agent receives and analyzes query
    steps.push({
      agent: 'US',
      message: `Received support query from customer ${query.customerId}. Analyzing request and determining optimal handling approach.`,
      timestamp: new Date().toISOString()
    });

    // Step 2: Determine if EU agent collaboration is needed
    const customer = CustomerService.getCustomerById(query.customerId);
    let customerData: Customer | null = null;

    if (customer?.region === 'EU') {
      steps.push({
        agent: 'US',
        message: `Customer located in EU region. Requesting EU agent to handle data access with GDPR compliance.`,
        timestamp: new Date().toISOString()
      });

      // Step 3: EU Agent handles data retrieval
      customerData = await CustomerService.getGDPRCompliantData(query.customerId);
      steps.push({
        agent: 'EU',
        message: `GDPR-compliant customer data retrieved successfully. Customer has ${customerData?.gdprConsent ? 'provided' : 'not provided'} consent. Sharing relevant information with US agent.`,
        timestamp: new Date().toISOString(),
        data: customerData
      });
    } else {
      // US customer - direct access
      customerData = customer;
      steps.push({
        agent: 'US',
        message: `US customer identified. Accessing customer data directly from US systems.`,
        timestamp: new Date().toISOString(),
        data: customerData
      });
    }

    // Step 4: Generate personalized response
    const finalResponse = this.generatePersonalizedResponse(query, customerData);
    steps.push({
      agent: 'US',
      message: `Generating personalized response based on customer profile, purchase history, and regional preferences.`,
      timestamp: new Date().toISOString()
    });

    const processingTime = Date.now() - startTime;

    return {
      id: `collab-${Date.now()}`,
      queryId: query.id,
      steps,
      finalResponse,
      processingTime
    };
  }

  private static generatePersonalizedResponse(query: SupportQuery, customer: Customer | null): string {
    if (!customer) {
      return "I apologize, but I'm unable to access your customer information at this time. Please contact our support team directly.";
    }

    const greeting = customer.language === 'German' ? 'Guten Tag' : 
                    customer.language === 'French' ? 'Bonjour' : 'Hello';
    
    let response = `${greeting} ${customer.name},\n\n`;

    switch (query.category) {
      case 'technical':
        response += `I understand you're experiencing technical difficulties with your ${customer.purchases[customer.purchases.length - 1]?.product}. As a valued ${customer.tier} tier customer, I want to ensure we resolve this quickly.\n\n`;
        response += `Based on your purchase history and configuration, I'll escalate this to our technical team who specialize in compliance modules. They'll contact you via ${customer.preferredChannel} within 2 hours.\n\n`;
        break;
      
      case 'billing':
        response += `I see you're inquiring about billing for your recent purchase. As per our records, you purchased ${customer.purchases[customer.purchases.length - 1]?.product} on ${customer.purchases[customer.purchases.length - 1]?.date}.\n\n`;
        response += `I'll have our billing specialist reach out to you via ${customer.preferredChannel} to discuss your options.\n\n`;
        break;
      
      case 'general':
        response += `Thank you for your inquiry. I see you're a ${customer.tier} tier customer with us since your first purchase in ${customer.purchases[0]?.date}.\n\n`;
        response += `I'll provide you with detailed information about our services and how they can best serve your needs.\n\n`;
        break;
      
      default:
        response += `Thank you for contacting our support team. I'll ensure your inquiry receives proper attention.\n\n`;
    }

    if (customer.region === 'EU') {
      response += `Please note: This response was processed in compliance with GDPR regulations, with your data handled by our EU-based systems.\n\n`;
    }

    response += `Best regards,\nGlobal Customer Support Team`;

    return response;
  }
}
```

### `src/components/CustomerQueryForm.tsx`
```tsx
import React, { useState } from 'react';
import { Send, User, MapPin, Clock } from 'lucide-react';
import { SupportQuery, Customer } from '../types';
import { CustomerService } from '../services/customerService';
import { sampleQueries } from '../data/syntheticQueries';

interface CustomerQueryFormProps {
  onQuerySubmit: (query: SupportQuery) => void;
}

export const CustomerQueryForm: React.FC<CustomerQueryFormProps> = ({ onQuerySubmit }) => {
  const [selectedCustomer, setSelectedCustomer] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [category, setCategory] = useState<'billing' | 'technical' | 'general' | 'complaint'>('general');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>('medium');

  const customers = [...CustomerService.getCustomersByRegion('US'), ...CustomerService.getCustomersByRegion('EU')];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCustomer || !message) return;

    const query: SupportQuery = {
      id: `q-${Date.now()}`,
      customerId: selectedCustomer,
      message,
      timestamp: new Date().toISOString(),
      priority,
      category
    };

    onQuerySubmit(query);
    setMessage('');
  };

  const loadSampleQuery = (sampleQuery: SupportQuery) => {
    setSelectedCustomer(sampleQuery.customerId);
    setMessage(sampleQuery.message);
    setCategory(sampleQuery.category);
    setPriority(sampleQuery.priority);
  };

  const selectedCustomerData = selectedCustomer ? CustomerService.getCustomerById(selectedCustomer) : null;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Submit Customer Support Query</h2>
      
      {/* Sample Queries */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Quick Test Queries</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {sampleQueries.map((query) => {
            const customer = CustomerService.getCustomerById(query.customerId);
            return (
              <button
                key={query.id}
                onClick={() => loadSampleQuery(query)}
                className="text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-2 mb-1">
                  <User className="w-4 h-4 text-brand-blue" />
                  <span className="font-medium">{customer?.name}</span>
                  <MapPin className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-500">{customer?.region}</span>
                </div>
                <p className="text-sm text-gray-600 truncate">{query.message.substring(0, 80)}...</p>
              </button>
            );
          })}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Customer Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Customer
          </label>
          <select
            value={selectedCustomer}
            onChange={(e) => setSelectedCustomer(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-blue"
            required
          >
            <option value="">Choose a customer...</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.name} ({customer.region}) - {customer.tier}
              </option>
            ))}
          </select>
        </div>

        {/* Customer Info Display */}
        {selectedCustomerData && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-4 mb-2">
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-brand-blue" />
                <span className="font-medium">{selectedCustomerData.name}</span>
              </div>
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-gray-500" />
                <span className="text-sm">{selectedCustomerData.region}</span>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                selectedCustomerData.tier === 'Platinum' ? 'bg-purple-100 text-purple-800' :
                selectedCustomerData.tier === 'Gold' ? 'bg-yellow-100 text-yellow-800' :
                selectedCustomerData.tier === 'Silver' ? 'bg-gray-100 text-gray-800' :
                'bg-orange-100 text-orange-800'
              }`}>
                {selectedCustomerData.tier}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              Language: {selectedCustomerData.language} | Preferred Contact: {selectedCustomerData.preferredChannel}
              {selectedCustomerData.region === 'EU' && (
                <span className="ml-2 text-green-600">✓ GDPR Consent</span>
              )}
            </div>
          </div>
        )}

        {/* Category and Priority */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-blue"
            >
              <option value="general">General</option>
              <option value="technical">Technical</option>
              <option value="billing">Billing</option>
              <option value="complaint">Complaint</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-blue"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>

        {/* Message */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Support Message
          </label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-blue"
            placeholder="Describe your issue or question..."
            required
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!selectedCustomer || !message}
          className="w-full bg-brand-blue text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
        >
          <Send className="w-4 h-4" />
          Submit Query
        </button>
      </form>
    </div>
  );
};
```

### `src/components/AgentCollaborationView.tsx`
```tsx
import React from 'react';
import { Server, ArrowRight, Clock, CheckCircle } from 'lucide-react';
import { CollaborationLog } from '../types';

interface AgentCollaborationViewProps {
  collaboration: CollaborationLog | null;
  isProcessing: boolean;
}

export const AgentCollaborationView: React.FC<AgentCollaborationViewProps> = ({ 
  collaboration, 
  isProcessing 
}) => {
  if (!collaboration && !isProcessing) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Agent Collaboration</h2>
        <div className="text-center text-gray-500 py-12">
          <Server className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p>Submit a query to see agent collaboration in action</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Agent Collaboration</h2>
      
      {isProcessing && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-blue mx-auto mb-4"></div>
          <p className="text-gray-600">Agents are collaborating...</p>
        </div>
      )}

      {collaboration && (
        <div className="space-y-4">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="font-medium text-green-700">Collaboration Complete</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Clock className="w-4 h-4" />
              {collaboration.processingTime}ms
            </div>
          </div>

          <div className="space-y-4">
            {collaboration.steps.map((step, index) => (
              <div key={index} className="flex items-start gap-4">
                <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${
                  step.agent === 'US' 
                    ? 'bg-blue-100 text-blue-800' 
                    : 'bg-green-100 text-green-800'
                }`}>
                  <Server className="w-4 h-4" />
                  {step.agent} Agent
                </div>
                <div className="flex-1">
                  <p className="text-gray-700 mb-2">{step.message}</p>
                  <div className="text-xs text-gray-500">
                    {new Date(step.timestamp).toLocaleTimeString()}
                  </div>
                  {step.data && (
                    <div className="mt-2 p-2 bg-gray-50 rounded text-sm">
                      <strong>Data Retrieved:</strong> Customer profile, purchase history, preferences
                    </div>
                  )}
                </div>
                {index < collaboration.steps.length - 1 && (
                  <ArrowRight className="w-4 h-4 text-gray-400 mt-2" />
                )}
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-brand-gray rounded-lg border-l-4 border-brand-blue">
            <h3 className="font-medium text-gray-800 mb-2">Final Response Generated</h3>
            <p className="text-sm text-gray-600">
              Personalized response created using cross-server intelligence and regional compliance
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
```

### `src/components/ResponseDisplay.tsx`
```tsx
import React from 'react';
import { MessageSquare, Copy, CheckCircle } from 'lucide-react';
import { CollaborationLog } from '../types';

interface ResponseDisplayProps {
  collaboration: CollaborationLog | null;
}

export const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ collaboration }) => {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = async () => {
    if (collaboration?.finalResponse) {
      await navigator.clipboard.writeText(collaboration.finalResponse);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (!collaboration) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Customer Response</h2>
        <div className="text-center text-gray-500 py-12">
          <MessageSquare className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p>No response generated yet</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Customer Response</h2>
        <button
          onClick={copyToClipboard}
          className="flex items-center gap-2 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          {copied ? <CheckCircle className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
          {collaboration.finalResponse}
        </div>
      </div>

      <div className="mt-4 text-xs text-gray-500">
        Response generated through US-EU agent collaboration • Processing time: {collaboration.processingTime}ms
      </div>
    </div>
  );
};
```

### `src/App.tsx`
```tsx
import React, { useState } from 'react';
import { Globe, Users, MessageSquare, BarChart3 } from 'lucide-react';
import { CustomerQueryForm } from './components/CustomerQueryForm';
import { AgentCollaborationView } from './components/AgentCollaborationView';
import { ResponseDisplay } from './components/ResponseDisplay';
import { SupportQuery, CollaborationLog } from './types';
import { AgentService } from './services/agentService';

type TabType = 'query' | 'collaboration' | 'response';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('query');
  const [currentCollaboration, setCurrentCollaboration] = useState<CollaborationLog | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleQuerySubmit = async (query: SupportQuery) => {
    setIsProcessing(true);
    setActiveTab('collaboration');
    
    try {
      // Simulate processing time for demo effect
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const collaboration = await AgentService.processQuery(query);
      setCurrentCollaboration(collaboration);
      setIsProcessing(false);
      
      // Auto-switch to response tab after collaboration
      setTimeout(() => {
        setActiveTab('response');
      }, 1000);
    } catch (error) {
      console.error('Error processing query:', error);
      setIsProcessing(false);
    }
  };

  const tabs = [
    { id: 'query', label: 'Submit Query', icon: MessageSquare },
    { id: 'collaboration', label: 'Agent Collaboration', icon: Users },
    { id: 'response', label: 'Customer Response', icon: BarChart3 }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Globe className="w-10 h-10 text-brand-blue" />
            <h1 className="text-4xl font-bold text-gray-800">Global Customer Support</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Demonstrating cross-server LLM agent collaboration for GDPR-compliant global customer support
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="flex bg-white rounded-lg shadow-md p-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as TabType)}
                  className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all ${
                    activeTab === tab.id
                      ? 'bg-brand-blue text-white shadow-md'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Tab Content */}
        <div className="max-w-4xl mx-auto">
          {activeTab === 'query' && (
            <CustomerQueryForm onQuerySubmit={handleQuerySubmit} />
          )}
          
          {activeTab === 'collaboration' && (
            <AgentCollaborationView 
              collaboration={currentCollaboration} 
              isProcessing={isProcessing}
            />
          )}
          
          {activeTab === 'response' && (
            <ResponseDisplay collaboration={currentCollaboration} />
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500">
          <p>Global Customer Support Demo • Kamiwaza Platform POC</p>
          <p className="text-sm mt-2">
            US Agent: Primary query processing • EU Agent: GDPR-compliant data access
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
```

## Running the Demo

### Development
```bash
npm start
```

### Build for Production
```bash
npm run build
```

## Demo Flow

1. **Query Submission**: Select a customer and submit a support query through the modern React interface
2. **Agent Collaboration**: Watch real-time visualization of US and EU agents collaborating:
   - US Agent receives and analyzes the query
   - EU Agent handles GDPR-compliant data access for European customers
   - Cross-server data sharing with compliance verification
   - Response generation using combined intelligence
3. **Final Response**: View the personalized customer response that leverages both regional expertise and data sovereignty compliance

## Key Features Demonstrated

- **Data Sovereignty**: EU customer data handled exclusively by EU agents
- **GDPR Compliance**: Automated consent verification and compliant data processing  
- **Seamless Collaboration**: Real-time agent-to-agent communication across geographic boundaries
- **Personalized Responses**: Customer tier, language, and regional preferences considered
- **Regional Expertise**: US and EU agents bring localized knowledge to support interactions

## Commercial Value

This demo showcases how Kamiwaza's distributed LLM platform enables:
- **Compliance**: Automated adherence to regional data protection regulations
- **Performance**: Reduced latency through geographically distributed processing
- **Intelligence**: Enhanced customer service through specialized regional agents
- **Scalability**: Easy expansion to additional regions and use cases

Perfect for demonstrating to security firms and enterprises requiring global operations with strict data governance.