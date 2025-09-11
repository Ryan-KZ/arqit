import React, { useState, useEffect } from 'react';
import { Server, ArrowRight, Clock, CheckCircle, Loader, Database, Shield, Zap, MessageSquare } from 'lucide-react';
import { CollaborationLog } from '../types';

interface AgentCollaborationViewProps {
  collaboration: CollaborationLog | null;
  isProcessing: boolean;
}

export const AgentCollaborationView: React.FC<AgentCollaborationViewProps> = ({ 
  collaboration, 
  isProcessing 
}) => {
  const [visibleSteps, setVisibleSteps] = useState<number>(0);

  // Animate steps appearing one by one
  useEffect(() => {
    if (collaboration?.steps) {
      let stepIndex = 0;
      const showStep = () => {
        if (stepIndex < collaboration.steps.length) {
          setVisibleSteps(stepIndex + 1);
          stepIndex++;
          setTimeout(showStep, 200); // Show each step with a delay
        }
      };
      setTimeout(showStep, 300); // Initial delay
    }
  }, [collaboration]);

  if (!collaboration && !isProcessing) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Agent Collaboration</h2>
        <div className="text-center text-gray-500 py-12">
          <Server className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <p>Submit a query to see multi-agent collaboration in action</p>
          <p className="text-sm mt-2">Watch US and EU agents work together in real-time</p>
        </div>
      </div>
    );
  }

  const getStepIcon = (message: string) => {
    if (message.includes('📥') || message.includes('Query received')) return MessageSquare;
    if (message.includes('🔍') || message.includes('database')) return Database;
    if (message.includes('🔒') || message.includes('🌍') || message.includes('GDPR')) return Shield;
    if (message.includes('⚡') || message.includes('✨')) return Zap;
    return Server;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Multi-Agent Collaboration</h2>
      
      {isProcessing && (
        <div className="space-y-6">
          <div className="text-center py-4">
            <div className="flex items-center justify-center mb-4">
              <Loader className="w-8 h-8 text-brand-blue animate-spin" />
            </div>
            <p className="text-gray-600 text-lg font-medium">Processing Multi-Region Collaboration</p>
            <p className="text-sm text-gray-500 mt-1">US and EU agents working together...</p>
          </div>
          
          {/* Enhanced Processing Animation */}
          <div className="relative">
            <div className="flex justify-between items-center mb-8">
              <div className="text-center flex-1">
                <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mb-3 mx-auto animate-pulse">
                  <Server className="w-10 h-10 text-blue-600" />
                </div>
                <p className="text-sm text-blue-600 font-bold">US Agent</p>
                <p className="text-xs text-blue-500">20.185.179.136</p>
                <div className="mt-2 px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs">
                  Query Processing
                </div>
              </div>
              
              <div className="flex-shrink-0 mx-4">
                <ArrowRight className="w-8 h-8 text-gray-400 animate-bounce" />
              </div>
              
              <div className="text-center flex-1">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-3 mx-auto animate-pulse">
                  <Server className="w-10 h-10 text-green-600" />
                </div>
                <p className="text-sm text-green-600 font-bold">EU Agent</p>
                <p className="text-xs text-green-500">9.163.149.120</p>
                <div className="mt-2 px-2 py-1 bg-green-50 text-green-700 rounded-full text-xs">
                  Data Compliance
                </div>
              </div>
            </div>
            
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center animate-spin">
                <Zap className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>
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
              {collaboration.processing_time}ms
            </div>
          </div>

          <div className="space-y-6">
            {collaboration.steps.slice(0, visibleSteps).map((step, index) => {
              const StepIcon = getStepIcon(step.message);
              const isAnimating = index === visibleSteps - 1;
              
              return (
                <div 
                  key={index} 
                  className={`transition-all duration-500 ${isAnimating ? 'animate-fade-in' : ''}`}
                >
                  <div className="flex items-start gap-4 p-4 rounded-lg border-l-4 border-gray-200 bg-gray-50 hover:bg-gray-100 transition-colors">
                    {/* Agent Badge */}
                    <div className={`flex items-center gap-2 px-3 py-2 rounded-full text-sm font-bold shadow-sm ${
                      step.agent === 'US' 
                        ? 'bg-blue-100 text-blue-800 border border-blue-200' 
                        : 'bg-green-100 text-green-800 border border-green-200'
                    }`}>
                      <StepIcon className="w-4 h-4" />
                      <span className="font-bold">
                        {step.agent} Agent
                      </span>
                    </div>

                    {/* Step Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between mb-2">
                        <p className="text-gray-800 font-medium leading-relaxed">{step.message}</p>
                        <span className="text-xs text-gray-500 ml-4 flex-shrink-0">
                          Step {index + 1}
                        </span>
                      </div>
                      
                      <div className="text-xs text-gray-500 mb-3">
                        ⏱️ {new Date(step.timestamp).toLocaleTimeString()}
                      </div>

                      {/* Enhanced Data Display */}
                      {step.data && (
                        <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3">
                          {step.data.query_analysis && (
                            <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                              <div className="font-semibold text-blue-800 text-sm mb-1">📋 Query Analysis</div>
                              <div className="text-xs text-blue-700">
                                Category: {step.data.query_analysis.category} | Priority: {step.data.query_analysis.priority}
                              </div>
                            </div>
                          )}
                          
                          {step.data.customer_data && (
                            <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                              <div className="font-semibold text-green-800 text-sm mb-1">👤 Customer Profile</div>
                              <div className="text-xs text-green-700">
                                {step.data.customer_data.name} • {step.data.customer_data.tier} Tier<br/>
                                Region: {step.data.customer_data.region} | GDPR: {step.data.customer_data.gdpr_consent ? '✅' : '❌'}
                              </div>
                            </div>
                          )}
                          
                          {step.data.database_query && (
                            <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                              <div className="font-semibold text-purple-800 text-sm mb-1">💾 Database Access</div>
                              <div className="text-xs text-purple-700">
                                Query: {step.data.database_query} | Status: {step.data.status}
                              </div>
                            </div>
                          )}
                          
                          {step.data.resolution_path && (
                            <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                              <div className="font-semibold text-yellow-800 text-sm mb-1">🎯 Resolution Path</div>
                              <div className="text-xs text-yellow-700">
                                Path: {step.data.resolution_path}<br/>
                                ETA: {step.data.estimated_resolution_time}
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Connection Line */}
                    {index < collaboration.steps.length - 1 && (
                      <div className="flex flex-col items-center ml-4">
                        <div className="w-px h-8 bg-gray-300"></div>
                        <ArrowRight className="w-5 h-5 text-gray-400 transform rotate-90" />
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
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