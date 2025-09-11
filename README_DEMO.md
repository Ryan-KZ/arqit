# Global Customer Support Demo

A comprehensive demonstration of multi-site agentic AI collaboration for customer support, showcasing data sovereignty compliance and seamless service delivery across US and EU regions.

## 🌍 Architecture Overview

- **US Agent** (20.185.179.136:61100): Primary query processing and response generation
- **EU Agent** (9.163.149.120:61102): GDPR-compliant data access for European customers
- **Flask API Backend**: Orchestrates agent collaboration and data flow
- **React TypeScript Frontend**: Interactive demo interface with real-time collaboration visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ with `uv` package manager
- Node.js 18+ with npm
- Access to the configured LLM endpoints

### Option 1: Automated Setup
```bash
# Run the demo launcher (recommended)
python start_demo.py
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Install Python dependencies
uv sync

# Start the API server
uv run api_server.py
```

#### Frontend Setup
```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start the React development server  
npm start
```

## 📋 Demo Workflow

### 1. Submit Customer Query
- Choose from sample queries or create custom ones
- Select customer (US or EU region)
- Set category (technical, billing, general, complaint) and priority

### 2. Watch Agent Collaboration
- **US Agent**: Analyzes incoming query and determines handling approach
- **EU Agent**: Provides GDPR-compliant data access for European customers
- **Cross-Region Data Sharing**: Secure, compliant information exchange
- **Response Generation**: Personalized responses using combined intelligence

### 3. View Final Response
- Personalized greeting in customer's preferred language
- Tier-appropriate service level (Bronze, Silver, Gold, Platinum)
- Purchase history and preference awareness
- GDPR compliance notifications for EU customers

## 🛡️ Key Features

### Data Sovereignty & Compliance
- **GDPR Compliance**: EU customer data stays in EU systems
- **Consent Verification**: Automatic GDPR consent checking
- **Regional Processing**: Data processed in appropriate geographic regions
- **Audit Trail**: Complete collaboration logging for compliance

### Intelligent Collaboration
- **Context Sharing**: Agents share relevant customer insights
- **Regional Expertise**: EU agents provide local regulatory knowledge
- **Seamless Handoffs**: Transparent collaboration between regions
- **Performance Optimization**: Sub-second response times

### Customer Experience
- **Personalization**: Responses tailored to customer tier and history
- **Multi-language Support**: Greetings in customer's preferred language
- **Channel Preferences**: Respects preferred contact methods
- **Contextual Responses**: Leverages purchase history and past interactions

## 📊 Sample Scenarios

### Technical Support (US Customer)
- **Customer**: Sarah Johnson (Gold tier, US)
- **Query**: Compliance module false positives
- **Flow**: US Agent → Direct data access → Personalized technical response
- **Result**: Tier-appropriate escalation with 2-hour SLA

### GDPR Inquiry (EU Customer)
- **Customer**: Hans Müller (Platinum tier, EU, German)
- **Query**: GDPR data processing requirements
- **Flow**: US Agent → EU Agent (GDPR compliance) → Multilingual response
- **Result**: German greeting + GDPR compliance confirmation

### Billing Request (EU Customer)
- **Customer**: Marie Dubois (Silver tier, EU, French)
- **Query**: Refund request for security package
- **Flow**: US Agent → EU Agent (data access) → Billing specialist referral
- **Result**: French greeting + GDPR-compliant billing review

## 🔧 Technical Details

### Backend Stack
- **CrewAI Framework**: Multi-agent orchestration
- **Flask API**: RESTful endpoints for frontend integration
- **Python Data Classes**: Type-safe data modeling
- **CORS Support**: Cross-origin resource sharing for development

### Frontend Stack
- **React 18**: Modern component architecture
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Consistent iconography

### API Endpoints
```
GET  /api/health                    # System health check
GET  /api/customers                 # List all customers
GET  /api/customers/:id             # Get specific customer
POST /api/support/query             # Submit support query
GET  /api/support/sample-queries    # Get sample test queries
GET  /api/agents/status             # Agent status and endpoints
```

## 🎯 Business Value Demonstration

### For Security Firms
- **Compliance Automation**: Reduces manual GDPR compliance overhead
- **Regional Expertise**: Local knowledge without physical presence
- **Audit Readiness**: Complete collaboration trails for regulatory review
- **Scalability**: Easy expansion to new regions and use cases

### For Enterprise Customers
- **Data Sovereignty**: Customer data never leaves required geographic boundaries
- **Service Quality**: Consistent, high-quality support across regions
- **Performance**: Fast response times through distributed processing
- **Transparency**: Visible collaboration process builds trust

## 🛠️ Development & Customization

### Adding New Regions
1. Configure new LLM endpoint in `customer_support.py`
2. Create region-specific agent with appropriate backstory
3. Update frontend to display new region in collaboration view
4. Add region-specific compliance requirements

### Extending Customer Data
1. Update data classes in `customer_support.py`
2. Modify synthetic customer data
3. Update TypeScript interfaces in `frontend/src/types/`
4. Enhance UI components to display new fields

### Custom Agent Behaviors
1. Modify agent roles and backstories in `GlobalCustomerSupportService`
2. Customize task descriptions for different query types
3. Add new collaboration steps or decision points
4. Update frontend visualization to reflect new flows

## 🔍 Monitoring & Observability

### Performance Metrics
- Query processing time (typically < 2 seconds)
- Agent response time per region
- Cross-region collaboration overhead
- Customer satisfaction indicators

### Compliance Tracking
- GDPR consent verification rates
- Data access audit logs
- Regional processing confirmation
- Compliance violation alerts

## 🤝 Demo Scenarios for Prospects

### Scenario 1: "Compliance First"
Show how EU customer data stays in EU systems while still enabling global support quality.

### Scenario 2: "Premium Experience"
Demonstrate tier-aware responses and how Platinum customers get different treatment than Bronze.

### Scenario 3: "Regulatory Intelligence"
Display how regional agents provide specialized knowledge (GDPR, local regulations).

### Scenario 4: "Scale Demonstration"
Process multiple queries simultaneously to show system performance.

## 📞 Support & Contact

This demo showcases the potential of distributed agentic AI systems for enterprise customer support. For questions about implementation, customization, or deployment:

- Review the technical documentation in the codebase
- Examine the API endpoints and data models
- Explore the React components for UI customization
- Test different customer scenarios and query types

---

**Built with**: CrewAI • React • TypeScript • Flask • Tailwind CSS  
**Demonstrates**: Multi-region AI collaboration • GDPR compliance • Personalized customer service