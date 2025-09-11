import React, { useState, useEffect } from 'react';
import { Send, User, MapPin, Clock } from 'lucide-react';
import { SupportQuery, Customer } from '../types';
import { apiService } from '../services/api';

interface CustomerQueryFormProps {
  onQuerySubmit: (query: SupportQuery) => void;
}

export const CustomerQueryForm: React.FC<CustomerQueryFormProps> = ({ onQuerySubmit }) => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [sampleQueries, setSampleQueries] = useState<any[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [category, setCategory] = useState<'billing' | 'technical' | 'general' | 'complaint'>('general');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>('medium');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [customersRes, queriesRes] = await Promise.all([
          apiService.getCustomers(),
          apiService.getSampleQueries()
        ]);
        
        setCustomers(customersRes.customers);
        setSampleQueries(queriesRes.queries);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCustomer || !message) return;

    const query: SupportQuery = {
      id: `q-${Date.now()}`,
      customer_id: selectedCustomer,
      message,
      timestamp: new Date().toISOString(),
      priority,
      category
    };

    onQuerySubmit(query);
    setMessage('');
  };

  const loadSampleQuery = (sampleQuery: any) => {
    setSelectedCustomer(sampleQuery.customer_id);
    setMessage(sampleQuery.message);
    setCategory(sampleQuery.category);
    setPriority(sampleQuery.priority);
  };

  const selectedCustomerData = selectedCustomer 
    ? customers.find(c => c.id === selectedCustomer) 
    : null;

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Submit Customer Support Query</h2>
      
      {/* Sample Queries */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Multi-Language Demo Queries</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {sampleQueries.map((query) => {
            const getLanguageFlag = (language: string) => {
              switch (language) {
                case 'German': return '🇩🇪';
                case 'Italian': return '🇮🇹';
                case 'French': return '🇫🇷';
                case 'English': return '🇺🇸';
                default: return '🌍';
              }
            };
            
            const getLanguageColor = (language: string) => {
              switch (language) {
                case 'German': return 'border-red-200 bg-red-50 hover:bg-red-100';
                case 'Italian': return 'border-green-200 bg-green-50 hover:bg-green-100';
                case 'French': return 'border-blue-200 bg-blue-50 hover:bg-blue-100';
                case 'English': return 'border-gray-200 bg-gray-50 hover:bg-gray-100';
                default: return 'border-gray-200 bg-gray-50 hover:bg-gray-100';
              }
            };

            return (
              <button
                key={query.id}
                onClick={() => loadSampleQuery(query)}
                className={`text-left p-4 border rounded-lg transition-all duration-200 transform hover:scale-105 ${getLanguageColor(query.customer?.language)}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-brand-blue" />
                    <span className="font-bold">{query.customer?.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{getLanguageFlag(query.customer?.language)}</span>
                    <span className="text-xs font-medium px-2 py-1 bg-white rounded-full">
                      {query.customer?.language}
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center gap-4 mb-2">
                  <div className="flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-gray-400" />
                    <span className="text-xs text-gray-500">{query.customer?.region}</span>
                  </div>
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                    query.customer?.tier === 'Platinum' ? 'bg-purple-100 text-purple-800' :
                    query.customer?.tier === 'Gold' ? 'bg-yellow-100 text-yellow-800' :
                    query.customer?.tier === 'Silver' ? 'bg-gray-200 text-gray-800' :
                    'bg-orange-100 text-orange-800'
                  }`}>
                    {query.customer?.tier}
                  </div>
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                    query.priority === 'high' ? 'bg-red-100 text-red-800' :
                    query.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {query.priority}
                  </div>
                </div>
                
                <p className="text-sm text-gray-700 line-clamp-2 leading-relaxed">
                  {query.message.length > 100 
                    ? `${query.message.substring(0, 100)}...` 
                    : query.message
                  }
                </p>
                
                <div className="mt-2 text-xs text-gray-500">
                  <span className="font-medium">Category:</span> {query.category}
                  {query.customer?.language !== 'English' && (
                    <span className="ml-3 text-blue-600 font-medium">
                      • Multi-language Response Demo
                    </span>
                  )}
                </div>
              </button>
            );
          })}
        </div>
        
        <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-blue-600">💡</span>
            <span className="font-medium text-blue-800">Multi-Language Demo Features</span>
          </div>
          <ul className="text-sm text-blue-700 space-y-1 ml-6">
            <li>• <span className="font-medium">German (🇩🇪)</span>: Native language query processing with GDPR compliance</li>
            <li>• <span className="font-medium">Italian (🇮🇹)</span>: Regional EU compliance with localized response</li>
            <li>• <span className="font-medium">Cross-Regional</span>: All queries trigger US ↔ EU agent collaboration</li>
          </ul>
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
              Language: {selectedCustomerData.language} | Preferred Contact: {selectedCustomerData.preferred_channel}
              {selectedCustomerData.region === 'EU' && selectedCustomerData.gdpr_consent && (
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