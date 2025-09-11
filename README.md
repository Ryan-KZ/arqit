# Global Customer Support Demo - Multi-Site Agentic Framework

A production-ready demonstration of cross-server LLM agent collaboration for GDPR-compliant global customer support, featuring real-time streaming updates and multi-language response generation.

## 🌍 Architecture Overview

This system demonstrates how AI agents deployed across different geographical regions can collaborate in real-time while respecting data sovereignty and compliance requirements.

### Agent Deployment
- **🇺🇸 US Agent**: Primary query processing & response generation
  - Endpoint: `http://20.185.179.136:61100/v1`
  - Model: Qwen2.5-7B-Instruct-GGUF (CPU-only)
  - Role: Customer Support Specialist

- **🇪🇺 EU Agent**: GDPR-compliant data access & compliance validation  
  - Endpoint: `http://9.163.149.120:61102/v1`
  - Model: Qwen2.5-7B-Instruct-GGUF (CPU-only)
  - Role: Data Compliance Specialist

### Technology Stack
- **Backend**: Python + Flask + CrewAI framework
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Package Manager**: uv (Python workspace management)
- **AI Framework**: CrewAI with custom LLM endpoints
- **Streaming**: Server-Sent Events (SSE) for real-time updates

## 🚀 Quick Start

### Prerequisites
- uv package manager installed
- Node.js 18+ for frontend
- Access to the deployed LLM endpoints (or modify endpoints in `customer_support.py`)

### Backend Setup
```bash
# Install dependencies
uv sync

# Start the API server
uv run api_server.py
```
Server will be available at `http://localhost:5001`

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start development server
SKIP_PREFLIGHT_CHECK=true npm start
```
Frontend will be available at `http://localhost:3000`

## 💡 Key Features

### Real-Time Multi-Agent Collaboration
- **Live Streaming**: Watch agents communicate in real-time via Server-Sent Events
- **Cross-Regional Processing**: US ↔ EU agent collaboration for every query
- **Progress Updates**: See each phase of LLM processing as it happens

### Multi-Language Support
- **Native Language Processing**: Queries in German, Italian, French automatically handled
- **Localized Responses**: Agents generate responses in customer's preferred language
- **Cultural Context**: Responses adapted for regional business practices

### GDPR Compliance
- **Data Sovereignty**: EU customer data processed by EU agents
- **Compliance Validation**: Automatic GDPR consent verification
- **Cross-Border Security**: Secure data sharing protocols between regions

### Customer Tier Management
- **Tier-Based Routing**: Platinum/Gold customers get specialized handling
- **Service Level Tracking**: Response times adapted to customer tier
- **Purchase History Integration**: Context-aware support based on customer profile

## 🎯 Demo Scenarios

### Sample Queries Available:
1. **English (US)**: General technical support and billing inquiries
2. **German (🇩🇪)**: "Guten Tag, ich habe Probleme mit der neuen Analytics-Module..."
3. **Italian (🇮🇹)**: "Buongiorno, vorrei sapere come posso aggiornare il mio piano attuale..."
4. **Multi-Regional**: Cross-border compliance and data sovereignty scenarios

### Real-Time Processing Flow:
1. 📥 **Query Reception**: Customer query analyzed by US Agent
2. 🧠 **US LLM Processing**: Initial analysis and collaboration decision
3. 🔒 **EU Agent Activation**: GDPR-compliant data access and validation
4. 💾 **EU LLM Processing**: Compliance verification and customer insights
5. ✨ **Response Generation**: Final multi-language response synthesis
6. 🎯 **Delivery**: Complete response with compliance confirmation

## 📁 Project Structure

```
arqit/
├── customer_support.py      # Core multi-agent system logic
├── api_server.py           # Flask REST API with streaming
├── main.py                 # Original story demo (converted from Jupyter)
├── frontend/               # React TypeScript application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   └── types/         # TypeScript type definitions
│   └── package.json       # Frontend dependencies
├── pyproject.toml         # Python project configuration
└── CLAUDE.md             # Development guidelines
```

## 🔧 Configuration

### LLM Endpoints
Modify endpoints in `customer_support.py`:
```python
# US Agent Configuration
llm_us = LLM(
    model="openai/Qwen2.5-7B-Instruct-GGUF",
    base_url="http://20.185.179.136:61100/v1",
    api_key="local"
)

# EU Agent Configuration  
llm_eu = LLM(
    model="openai/Qwen2.5-7B-Instruct-GGUF",
    base_url="http://9.163.149.120:61102/v1",
    api_key="local"
)
```

### Customer Data
Sample customers with different tiers and regions are defined in `CustomerService.CUSTOMERS`. Modify as needed for your demo scenarios.

## 🌐 API Endpoints

### REST API
- `GET /api/health` - Health check
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get specific customer
- `POST /api/support/query` - Submit support query (blocking)
- `POST /api/support/query-stream` - Submit query with real-time streaming
- `GET /api/support/sample-queries` - Get demo queries
- `GET /api/agents/status` - Agent status and endpoints

### Streaming API
The `/api/support/query-stream` endpoint provides real-time updates:
```javascript
// Example streaming response
data: {"type": "step", "step": {"agent": "US", "message": "📥 Starting analysis..."}}
data: {"type": "step", "step": {"agent": "EU", "message": "🔒 EU Agent connecting..."}}
data: {"type": "complete", "collaboration": {"final_response": "...", "processing_time": 280745}}
```

## 🧪 Testing

### Manual Testing
Use the frontend interface to test various scenarios:
1. Select different customer profiles (US/EU, different tiers)
2. Try sample queries in multiple languages
3. Watch real-time collaboration unfold
4. Verify appropriate response language and compliance notes

### API Testing
```bash
# Test streaming endpoint
curl -X POST http://localhost:5001/api/support/query-stream \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust-eu-004", "message": "Test query", "category": "general", "priority": "medium"}' \
  --no-buffer
```

## 🔒 Security & Compliance

- **Data Sovereignty**: Customer data processed in appropriate regions
- **GDPR Compliance**: EU customers get GDPR-compliant processing
- **Secure Communications**: Cross-agent data sharing protocols
- **Access Control**: Tier-based service level management
- **Audit Trail**: Complete collaboration logs for compliance tracking

## 🚀 Performance

- **CPU-Only LLM Processing**: Optimized for CPU-only inference
- **Processing Time**: 280+ seconds for complex multi-agent tasks (realistic for CPU inference)
- **Streaming Updates**: Real-time progress prevents user timeout concerns
- **Concurrent Handling**: Multiple customer queries handled simultaneously

## 📊 Monitoring

The system provides detailed logging:
- Agent task execution progress
- LLM response times
- Cross-agent collaboration steps
- Customer interaction patterns
- Compliance verification results

## 🛠️ Development

This project follows the guidelines in `CLAUDE.md`:
- Task-based development with vertical slices
- Real LLM integration (no mocked responses)
- Production-ready code patterns
- Comprehensive error handling

### Key Development Decisions:
- **Real vs Simulated**: Uses actual LLM endpoints for authentic performance
- **Streaming vs Blocking**: Implements both for different use cases
- **Multi-Language**: Native language support without translation layers
- **Compliance-First**: Built with GDPR and data sovereignty as core requirements

## 📈 Future Enhancements

Potential extensions:
- Additional language support (Spanish, Chinese, etc.)
- More sophisticated routing algorithms
- Enhanced compliance reporting
- Integration with external CRM systems
- Advanced analytics and insights
- Custom model fine-tuning for domain expertise

---

**Demo Status**: ✅ Production Ready
**Last Updated**: September 2025
**LLM Processing**: Real endpoints with CPU-only inference
**Multi-Language**: German, Italian, French, English supported
**Compliance**: GDPR-ready with data sovereignty handling
