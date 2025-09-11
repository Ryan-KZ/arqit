import React, { useState } from 'react';
import { Globe, Users, MessageSquare, BarChart3, AlertCircle } from 'lucide-react';
import { CustomerQueryForm } from './components/CustomerQueryForm';
import { AgentCollaborationView } from './components/AgentCollaborationView';
import { ResponseDisplay } from './components/ResponseDisplay';
import { SupportQuery, CollaborationLog } from './types';
import { apiService } from './services/api';

type TabType = 'query' | 'collaboration' | 'response';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('query');
  const [currentCollaboration, setCurrentCollaboration] = useState<CollaborationLog | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleQuerySubmit = async (query: SupportQuery) => {
    setError(null);
    setIsProcessing(true);
    setCurrentCollaboration(null); // Clear previous collaboration
    setActiveTab('collaboration');
    
    try {
      // Use streaming API for real-time updates
      await apiService.submitQueryStreaming(
        {
          customer_id: query.customer_id,
          message: query.message,
          category: query.category,
          priority: query.priority
        },
        // onStep callback - receives real-time step updates
        (step) => {
          setCurrentCollaboration(prev => {
            const steps = prev?.steps || [];
            return {
              id: prev?.id || `temp-${Date.now()}`,
              query_id: query.id,
              steps: [...steps, step],
              final_response: prev?.final_response || '',
              processing_time: prev?.processing_time || 0
            };
          });
        },
        // onComplete callback - receives final result
        (collaboration) => {
          setCurrentCollaboration(prev => ({
            ...collaboration,
            steps: prev?.steps || [] // Keep the steps we've been building
          }));
          setIsProcessing(false);
          
          // Auto-switch to response tab after collaboration
          setTimeout(() => {
            setActiveTab('response');
          }, 1500);
        },
        // onError callback
        (errorMessage) => {
          console.error('Streaming query failed:', errorMessage);
          setError(errorMessage);
          setIsProcessing(false);
        }
      );
    } catch (error) {
      console.error('Error processing query:', error);
      setError(error instanceof Error ? error.message : 'An error occurred processing your query');
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
          <div className="mt-4 flex items-center justify-center gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span>US Agent: 20.185.179.136</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>EU Agent: 9.163.149.120</span>
            </div>
          </div>
        </header>

        {/* Error Display */}
        {error && (
          <div className="max-w-4xl mx-auto mb-6">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
              <div>
                <p className="text-red-800 font-medium">Error Processing Query</p>
                <p className="text-red-700 text-sm">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-500 hover:text-red-700"
              >
                ×
              </button>
            </div>
          </div>
        )}

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
          <p className="font-medium">Global Customer Support Demo • Multi-site Agentic Framework</p>
          <p className="text-sm mt-2">
            US Agent: Primary query processing & response generation • EU Agent: GDPR-compliant data access
          </p>
          <div className="mt-4 text-xs">
            <p>Powered by CrewAI • React + TypeScript • Flask API</p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;