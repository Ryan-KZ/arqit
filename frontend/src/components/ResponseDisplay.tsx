import React from 'react';
import { MessageSquare, Copy, CheckCircle, Globe } from 'lucide-react';
import { CollaborationLog } from '../types';

interface ResponseDisplayProps {
  collaboration: CollaborationLog | null;
}

export const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ collaboration }) => {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = async () => {
    if (collaboration?.final_response) {
      await navigator.clipboard.writeText(collaboration.final_response);
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
          <p className="text-sm mt-2">Submit a query to see personalized customer responses</p>
        </div>
      </div>
    );
  }

  // Determine if this was a cross-region collaboration
  const hadEuCollaboration = collaboration.steps.some(step => step.agent === 'EU');

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

      {/* Response Quality Indicators */}
      <div className="mb-4 flex flex-wrap gap-2">
        <div className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
          <Globe className="w-3 h-3" />
          Multi-Region
        </div>
        {hadEuCollaboration && (
          <div className="flex items-center gap-1 px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
            <CheckCircle className="w-3 h-3" />
            GDPR Compliant
          </div>
        )}
        <div className="flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs">
          <MessageSquare className="w-3 h-3" />
          Personalized
        </div>
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
          {collaboration.final_response}
        </div>
      </div>

      <div className="mt-4 text-xs text-gray-500 flex items-center justify-between">
        <span>
          Response generated through {hadEuCollaboration ? 'US-EU' : 'US'} agent collaboration
        </span>
        <span>
          Processing time: {collaboration.processing_time}ms
        </span>
      </div>

      {/* Response Analysis */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
        <h4 className="font-medium text-blue-900 mb-1">Response Features</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Personalized greeting and customer recognition</li>
          <li>• Tier-appropriate service level</li>
          <li>• Regional preference consideration</li>
          {hadEuCollaboration && <li>• GDPR-compliant data processing</li>}
          <li>• Clear next steps and contact method</li>
        </ul>
      </div>
    </div>
  );
};