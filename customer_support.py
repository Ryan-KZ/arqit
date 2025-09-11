#!/usr/bin/env python3
"""
Global Customer Support Demo using Multi-site CrewAI Agents
Extends the original agentic framework for customer support scenarios.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from crewai import Agent, Crew, Process, Task, LLM


@dataclass
class Purchase:
    id: str
    product: str
    amount: float
    date: str
    status: str  # completed, pending, refunded


@dataclass
class Customer:
    id: str
    name: str
    email: str
    region: str  # US, EU
    tier: str  # Bronze, Silver, Gold, Platinum
    language: str
    gdpr_consent: bool
    last_contact: str
    preferred_channel: str  # email, phone, chat
    purchases: List[Purchase]


@dataclass
class SupportQuery:
    id: str
    customer_id: str
    message: str
    timestamp: str
    priority: str  # low, medium, high, urgent
    category: str  # billing, technical, general, complaint


@dataclass
class AgentResponse:
    agent: str  # US, EU
    message: str
    timestamp: str
    data: Optional[Dict[str, Any]] = None


@dataclass
class CollaborationLog:
    id: str
    query_id: str
    steps: List[AgentResponse]
    final_response: str
    processing_time: int


class CustomerService:
    """Service for managing customer data with GDPR compliance."""
    
    # Synthetic customer data
    CUSTOMERS = [
        Customer(
            id="cust-us-001",
            name="Sarah Johnson",
            email="sarah.johnson@email.com",
            region="US",
            tier="Gold",
            language="English",
            gdpr_consent=False,
            last_contact="2024-09-05T14:30:00Z",
            preferred_channel="email",
            purchases=[
                Purchase("p1", "Enterprise Security Suite", 2500.0, "2024-08-15", "completed"),
                Purchase("p2", "Compliance Module", 800.0, "2024-09-01", "completed")
            ]
        ),
        Customer(
            id="cust-eu-001",
            name="Hans Müller",
            email="hans.mueller@email.de",
            region="EU",
            tier="Platinum",
            language="German",
            gdpr_consent=True,
            last_contact="2024-09-08T09:15:00Z",
            preferred_channel="phone",
            purchases=[
                Purchase("p3", "Advanced Threat Detection", 5000.0, "2024-07-20", "completed"),
                Purchase("p4", "GDPR Compliance Tools", 1200.0, "2024-08-30", "completed")
            ]
        ),
        Customer(
            id="cust-eu-002",
            name="Marie Dubois",
            email="marie.dubois@email.fr",
            region="EU",
            tier="Silver",
            language="French",
            gdpr_consent=True,
            last_contact="2024-09-10T16:45:00Z",
            preferred_channel="chat",
            purchases=[
                Purchase("p5", "Basic Security Package", 1000.0, "2024-08-25", "completed")
            ]
        ),
        Customer(
            id="cust-eu-003",
            name="Klaus Weber",
            email="klaus.weber@email.de",
            region="EU",
            tier="Platinum",
            language="German",
            gdpr_consent=True,
            last_contact="2024-09-11T08:30:00Z",
            preferred_channel="email",
            purchases=[
                Purchase("p7", "Enterprise Security Suite", 3500.0, "2024-08-20", "completed"),
                Purchase("p8", "Advanced Analytics Module", 1500.0, "2024-09-05", "completed")
            ]
        ),
        Customer(
            id="cust-eu-004",
            name="Marco Rossi",
            email="marco.rossi@email.it",
            region="EU",
            tier="Gold",
            language="Italian",
            gdpr_consent=True,
            last_contact="2024-09-09T14:15:00Z",
            preferred_channel="phone",
            purchases=[
                Purchase("p9", "Professional Security Tools", 2200.0, "2024-08-28", "completed"),
                Purchase("p10", "Compliance Dashboard", 800.0, "2024-09-02", "completed")
            ]
        ),
        Customer(
            id="cust-us-002",
            name="Robert Chen",
            email="robert.chen@email.com",
            region="US",
            tier="Bronze",
            language="English",
            gdpr_consent=False,
            last_contact="2024-09-03T11:20:00Z",
            preferred_channel="email",
            purchases=[
                Purchase("p6", "Starter Security Tools", 500.0, "2024-08-10", "completed")
            ]
        )
    ]
    
    @classmethod
    def get_customer_by_id(cls, customer_id: str) -> Optional[Customer]:
        """Retrieve customer by ID."""
        return next((c for c in cls.CUSTOMERS if c.id == customer_id), None)
    
    @classmethod
    def get_customers_by_region(cls, region: str) -> List[Customer]:
        """Get all customers in a specific region."""
        return [c for c in cls.CUSTOMERS if c.region == region]
    
    @classmethod
    def get_gdpr_compliant_data(cls, customer_id: str) -> Optional[Customer]:
        """Get customer data with GDPR compliance check."""
        customer = cls.get_customer_by_id(customer_id)
        if customer and customer.region == "EU" and customer.gdpr_consent:
            return customer
        elif customer and customer.region == "US":
            return customer
        return None


class GlobalCustomerSupportService:
    """Main service for processing customer support queries using multi-site agents."""
    
    def __init__(self):
        # Initialize LLM objects for our custom endpoints
        self.llm_eu = LLM(
            model="openai/Qwen2.5-7B-Instruct-GGUF",
            base_url="http://9.163.149.120:61102/v1",
            api_key="local"
        )
        
        self.llm_usa = LLM(
            model="openai/Qwen2.5-7B-Instruct-GGUF",
            base_url="http://20.185.179.136:61100/v1",
            api_key="local"
        )
        
        # Create specialized customer support agents
        self.us_agent = Agent(
            role="US Customer Support Specialist",
            goal="Provide excellent customer support while coordinating with EU agents for global customers",
            backstory=(
                "You are a skilled US-based customer support specialist with expertise in "
                "analyzing customer inquiries, determining appropriate response strategies, "
                "and coordinating with international teams. You handle initial query processing "
                "and craft final personalized responses for all customers."
            ),
            llm=self.llm_usa,
            verbose=True,
            allow_delegation=False
        )
        
        self.eu_agent = Agent(
            role="EU Customer Data Specialist",
            goal="Handle GDPR-compliant data access and provide regional expertise for European customers",
            backstory=(
                "You are a GDPR compliance expert and customer data specialist based in the EU. "
                "Your role is to safely access and process European customer data while ensuring "
                "full compliance with data protection regulations. You provide regional insights "
                "and customer context to support global customer service efforts."
            ),
            llm=self.llm_eu,
            verbose=True,
            allow_delegation=False
        )
    
    def process_query(self, query: SupportQuery) -> CollaborationLog:
        """Process a customer support query using REAL agent collaboration with LLM endpoints."""
        start_time = datetime.now()
        steps = []
        
        # Get customer information
        customer = CustomerService.get_customer_by_id(query.customer_id)
        if not customer:
            return self._create_error_response(query, "Customer not found")
        
        # Step 1: US Agent analyzes the query (REAL LLM CALL)
        steps.append(AgentResponse(
            agent="US",
            message=f"📥 Analyzing query from {customer.name} ({customer.region}). Calling US LLM endpoint...",
            timestamp=datetime.now().isoformat(),
            data={"query_analysis": {"category": query.category, "priority": query.priority, "customer_region": customer.region}}
        ))
        
        analysis_task = Task(
            description=(
                f"You are a US-based customer support specialist. Analyze this support query:\n\n"
                f"Customer: {customer.name} ({customer.region})\n"
                f"Tier: {customer.tier} | Language: {customer.language}\n"
                f"Query: {query.message}\n"
                f"Category: {query.category} | Priority: {query.priority}\n\n"
                f"Provide your initial analysis and determine if we need EU agent collaboration "
                f"for this {'EU' if customer.region == 'EU' else 'US'} customer. "
                f"Consider data sovereignty and GDPR requirements."
            ),
            expected_output="Initial query analysis with collaboration recommendation",
            agent=self.us_agent
        )
        
        # FORCE EU collaboration for ALL queries (demo purposes)
        steps.append(AgentResponse(
            agent="US", 
            message=f"🌍 Requesting EU agent collaboration for {'GDPR compliance' if customer.region == 'EU' else 'cross-regional validation'}. Establishing secure connection to EU endpoint...",
            timestamp=datetime.now().isoformat()
        ))
        
        # Step 2: EU Agent data access and validation (REAL LLM CALL)
        steps.append(AgentResponse(
            agent="EU",
            message=f"🔒 EU Agent responding. Calling EU LLM endpoint for {'GDPR-compliant data access' if customer.region == 'EU' else 'security validation'}...",
            timestamp=datetime.now().isoformat()
        ))
        
        eu_task_description = (
            f"You are an EU-based compliance and data specialist. "
            f"Customer: {customer.name} ({customer.region}) - {customer.tier} tier\n"
            f"Language: {customer.language} | GDPR Consent: {customer.gdpr_consent}\n"
            f"Query: {query.message}\n\n"
        )
        
        if customer.region == "EU":
            eu_task_description += (
                f"This EU customer requires GDPR-compliant data handling. "
                f"Provide customer insights while ensuring data protection compliance. "
                f"Include tier analysis, purchase history context, and regional considerations."
            )
        else:
            eu_task_description += (
                f"This US customer query requires cross-regional security validation. "
                f"Provide security assessment and any EU-relevant compliance insights."
            )
            
        data_access_task = Task(
            description=eu_task_description,
            expected_output="Customer data analysis with compliance confirmation",
            agent=self.eu_agent
        )
        
        # Step 3: Final response generation (REAL LLM CALL)
        steps.append(AgentResponse(
            agent="US",
            message=f"✨ Generating personalized response using multi-agent intelligence. Calling US LLM endpoint for final response...",
            timestamp=datetime.now().isoformat()
        ))
        
        response_task = Task(
            description=(
                f"Generate a personalized customer support response in {customer.language}:\n\n"
                f"Customer Details:\n"
                f"- Name: {customer.name}\n"
                f"- Region: {customer.region}\n" 
                f"- Tier: {customer.tier}\n"
                f"- Language: {customer.language}\n"
                f"- Preferred Contact: {customer.preferred_channel}\n"
                f"- GDPR Consent: {customer.gdpr_consent}\n\n"
                f"Query Information:\n"
                f"- Message: {query.message}\n"
                f"- Category: {query.category}\n"
                f"- Priority: {query.priority}\n\n"
                f"IMPORTANT RESPONSE REQUIREMENTS:\n"
                f"1. Write the ENTIRE response in {customer.language} (not English)\n"
                f"2. Use appropriate business greeting for {customer.language}\n"
                f"3. Reference their {customer.tier} tier status appropriately\n"
                f"4. Include next steps via their preferred {customer.preferred_channel} channel\n"
                f"5. Add GDPR compliance note if EU customer\n"
                f"6. Mention this response was created through US-EU collaboration\n\n"
                f"Use context from previous agent analysis to inform your response."
            ),
            expected_output=f"Complete customer support response written in {customer.language}",
            agent=self.us_agent,
            context=[analysis_task, data_access_task]
        )
        
        # Create and execute the crew (THIS MAKES REAL LLM CALLS)
        crew = Crew(
            agents=[self.us_agent, self.eu_agent],
            tasks=[analysis_task, data_access_task, response_task],
            process=Process.sequential,
            verbose=True,
            memory=False
        )
        
        # Execute the collaboration (REAL LLM PROCESSING - WILL BE SLOW)
        print(f"🚀 Starting REAL LLM collaboration for {customer.name}...")
        result = crew.kickoff()
        print(f"✅ LLM collaboration completed!")
        
        # Add final completion step
        steps.append(AgentResponse(
            agent="US",
            message=f"🎯 Multi-agent collaboration completed. Final response generated in {customer.language} with {customer.region} compliance.",
            timestamp=datetime.now().isoformat(),
            data={"customer_data": asdict(customer), "resolution_path": f"{query.category}_tier_{customer.tier.lower()}"}
        ))
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return CollaborationLog(
            id=f"real-collab-{int(datetime.now().timestamp())}",
            query_id=query.id,
            steps=steps,
            final_response=str(result),
            processing_time=processing_time
        )
    
    def _create_error_response(self, query: SupportQuery, error_message: str) -> CollaborationLog:
        """Create an error response when query processing fails."""
        return CollaborationLog(
            id=f"error-{int(datetime.now().timestamp())}",
            query_id=query.id,
            steps=[AgentResponse(
                agent="US",
                message=f"Error processing query: {error_message}",
                timestamp=datetime.now().isoformat()
            )],
            final_response=f"I apologize, but I encountered an error processing your request: {error_message}. Please try again or contact our support team directly.",
            processing_time=0
        )
    
    def process_query_with_demo_steps(self, query: SupportQuery) -> CollaborationLog:
        """
        Enhanced demo processing that forces multi-agent collaboration for ALL queries
        and shows detailed step-by-step interaction for demonstration purposes.
        """
        import time
        start_time = datetime.now()
        steps = []
        
        # Get customer information
        customer = CustomerService.get_customer_by_id(query.customer_id)
        if not customer:
            return self._create_error_response(query, "Customer not found")
        
        # Step 1: US Agent receives and analyzes query
        time.sleep(0.5)  # Simulate processing time
        steps.append(AgentResponse(
            agent="US",
            message=f"📥 Query received from {customer.name} ({customer.region}). Initial analysis: {query.category} issue with {query.priority} priority. Starting multi-region collaboration protocol...",
            timestamp=datetime.now().isoformat(),
            data={"query_analysis": {"category": query.category, "priority": query.priority, "customer_region": customer.region}}
        ))
        
        # Step 2: US Agent initiates database lookup
        time.sleep(0.7)
        steps.append(AgentResponse(
            agent="US",
            message=f"🔍 Initiating customer database lookup for {customer.id}. Checking regional data access requirements and compliance protocols...",
            timestamp=datetime.now().isoformat(),
            data={"database_query": "customer_profile", "status": "initiated"}
        ))
        
        # Step 3: ALWAYS involve EU Agent for enhanced collaboration demo
        time.sleep(0.6)
        eu_reason = "GDPR compliance verification" if customer.region == "EU" else "cross-regional data validation and security consultation"
        steps.append(AgentResponse(
            agent="US",
            message=f"🌍 Requesting EU agent collaboration for {eu_reason}. Establishing secure cross-region communication channel...",
            timestamp=datetime.now().isoformat()
        ))
        
        # Step 4: EU Agent responds and processes
        time.sleep(0.8)
        eu_message = f"🔒 EU Agent online. Processing {eu_reason} for customer {customer.id}." 
        if customer.region == "EU":
            eu_message += f" GDPR consent status: {'✅ Verified' if customer.gdpr_consent else '⚠️ Limited access'}. Accessing EU customer database..."
        else:
            eu_message += f" Cross-validating US customer data against EU security protocols. Checking for any EU-related transaction history..."
        
        steps.append(AgentResponse(
            agent="EU",
            message=eu_message,
            timestamp=datetime.now().isoformat(),
            data={"gdpr_check": customer.gdpr_consent, "data_access": "compliant", "customer_data": asdict(customer)}
        ))
        
        # Step 5: EU Agent provides additional insights
        time.sleep(0.5)
        if customer.tier in ["Platinum", "Gold"]:
            tier_insight = "Premium customer - escalating to specialized support team"
        else:
            tier_insight = "Standard support workflow initiated"
            
        steps.append(AgentResponse(
            agent="EU",
            message=f"📊 Customer analysis complete. Tier status: {customer.tier} ({tier_insight}). Purchase history: {len(customer.purchases)} products. Last contact: {customer.last_contact}. Sharing insights with US agent...",
            timestamp=datetime.now().isoformat(),
            data={"tier_analysis": customer.tier, "purchase_count": len(customer.purchases)}
        ))
        
        # Step 6: Cross-agent data correlation  
        time.sleep(0.4)
        steps.append(AgentResponse(
            agent="US",
            message=f"🔄 Received EU agent insights. Correlating customer data with query context. Analyzing {query.category} issue against customer's {customer.purchases[-1].product if customer.purchases else 'no recent purchases'} configuration...",
            timestamp=datetime.now().isoformat()
        ))
        
        # Step 7: Joint solution analysis
        time.sleep(0.9)
        steps.append(AgentResponse(
            agent="EU" if customer.region == "EU" else "US",
            message=f"⚡ Joint analysis complete. Issue classification: {query.category}. Recommended resolution path determined based on customer tier ({customer.tier}) and regional requirements. Preparing personalized response...",
            timestamp=datetime.now().isoformat(),
            data={"resolution_path": f"{query.category}_tier_{customer.tier.lower()}", "estimated_resolution_time": "2-4 hours"}
        ))
        
        # Step 8: Final response generation
        time.sleep(0.6)
        steps.append(AgentResponse(
            agent="US",
            message=f"✨ Generating personalized response using multi-agent intelligence. Incorporating regional preferences, tier-specific service levels, and cross-validated customer insights...",
            timestamp=datetime.now().isoformat()
        ))
        
        # Generate final response using existing logic
        final_response = self.generate_enhanced_personalized_response(query, customer, steps)
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return CollaborationLog(
            id=f"demo-collab-{int(datetime.now().timestamp())}",
            query_id=query.id,
            steps=steps,
            final_response=final_response,
            processing_time=processing_time
        )
    
    def process_query_stream(self, query: SupportQuery):
        """Generator that yields REAL-TIME collaboration steps during actual LLM processing."""
        start_time = datetime.now()
        customer = CustomerService.get_customer_by_id(query.customer_id)
        
        if not customer:
            yield {"error": "Customer not found", "timestamp": datetime.now().isoformat()}
            return
        
        # Step 1: Initial query processing
        yield {
            "type": "step",
            "step": {
                "agent": "US",
                "message": f"📥 Starting analysis of query from {customer.name} ({customer.region}). Initializing US LLM endpoint connection...",
                "timestamp": datetime.now().isoformat(),
                "data": {"query_analysis": {"category": query.category, "priority": query.priority, "customer_region": customer.region}}
            }
        }
        
        # Step 2: Create and execute US Agent analysis task  
        yield {
            "type": "step", 
            "step": {
                "agent": "US",
                "message": f"🧠 Calling US LLM (20.185.179.136:61100) for query analysis. Processing customer tier: {customer.tier}, Language: {customer.language}...",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        analysis_task = Task(
            description=(
                f"You are a US-based customer support specialist. Analyze this support query:\n\n"
                f"Customer: {customer.name} ({customer.region})\n"
                f"Tier: {customer.tier} | Language: {customer.language}\n"
                f"Query: {query.message}\n"
                f"Category: {query.category} | Priority: {query.priority}\n\n"
                f"Provide your initial analysis and determine if we need EU agent collaboration "
                f"for this {'EU' if customer.region == 'EU' else 'US'} customer. "
                f"Consider data sovereignty and GDPR requirements."
            ),
            expected_output="Initial query analysis with collaboration recommendation",
            agent=self.us_agent
        )
        
        # Execute US analysis task individually
        crew_analysis = Crew(
            agents=[self.us_agent],
            tasks=[analysis_task], 
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        print(f"🚀 Executing US Agent analysis task...")
        us_analysis = crew_analysis.kickoff()
        print(f"✅ US Agent analysis completed!")
        
        # Step 3: US Agent completed analysis
        yield {
            "type": "step",
            "step": {
                "agent": "US", 
                "message": f"✅ US LLM analysis completed. Initiating EU agent collaboration for {'GDPR compliance' if customer.region == 'EU' else 'cross-regional validation'}...",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Step 4: EU Agent data access
        yield {
            "type": "step",
            "step": {
                "agent": "EU",
                "message": f"🔒 EU Agent connecting. Calling EU LLM (9.163.149.120:61102) for {'GDPR-compliant data access' if customer.region == 'EU' else 'security validation'}...",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        eu_task_description = (
            f"You are an EU-based compliance and data specialist. "
            f"Customer: {customer.name} ({customer.region}) - {customer.tier} tier\n"
            f"Language: {customer.language} | GDPR Consent: {customer.gdpr_consent}\n"
            f"Query: {query.message}\n\n"
        )
        
        if customer.region == "EU":
            eu_task_description += (
                f"This EU customer requires GDPR-compliant data handling. "
                f"Provide customer insights while ensuring data protection compliance. "
                f"Include tier analysis, purchase history context, and regional considerations."
            )
        else:
            eu_task_description += (
                f"This US customer query requires cross-regional security validation. "
                f"Provide security assessment and any EU-relevant compliance insights."
            )
            
        data_access_task = Task(
            description=eu_task_description,
            expected_output="Customer data analysis with compliance confirmation",
            agent=self.eu_agent
        )
        
        # Execute EU data access task individually
        crew_eu = Crew(
            agents=[self.eu_agent],
            tasks=[data_access_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        print(f"🚀 Executing EU Agent data access task...")
        eu_analysis = crew_eu.kickoff()
        print(f"✅ EU Agent analysis completed!")
        
        # Step 5: EU Agent completed analysis
        yield {
            "type": "step",
            "step": {
                "agent": "EU",
                "message": f"✅ EU LLM analysis completed. Customer data processed with compliance verification. Sharing insights with US agent...",
                "timestamp": datetime.now().isoformat(),
                "data": {"gdpr_check": customer.gdpr_consent, "data_access": "compliant", "customer_data": asdict(customer)}
            }
        }
        
        # Step 6: Final response generation
        yield {
            "type": "step",
            "step": {
                "agent": "US",
                "message": f"✨ Generating personalized response in {customer.language}. Combining US analysis + EU compliance data. Calling US LLM for final response...",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        response_task = Task(
            description=(
                f"Generate a personalized customer support response in {customer.language}:\n\n"
                f"Customer Details:\n"
                f"- Name: {customer.name}\n"
                f"- Region: {customer.region}\n" 
                f"- Tier: {customer.tier}\n"
                f"- Language: {customer.language}\n"
                f"- Preferred Contact: {customer.preferred_channel}\n"
                f"- GDPR Consent: {customer.gdpr_consent}\n\n"
                f"Query Information:\n"
                f"- Message: {query.message}\n"
                f"- Category: {query.category}\n"
                f"- Priority: {query.priority}\n\n"
                f"Previous Analysis Context:\n"
                f"- US Agent Analysis: {str(us_analysis)[:200]}...\n"
                f"- EU Agent Analysis: {str(eu_analysis)[:200]}...\n\n"
                f"IMPORTANT RESPONSE REQUIREMENTS:\n"
                f"1. Write the ENTIRE response in {customer.language} (not English)\n"
                f"2. Use appropriate business greeting for {customer.language}\n"
                f"3. Reference their {customer.tier} tier status appropriately\n"
                f"4. Include next steps via their preferred {customer.preferred_channel} channel\n"
                f"5. Add GDPR compliance note if EU customer\n"
                f"6. Mention this response was created through US-EU collaboration\n\n"
                f"Create ONE cohesive response (not duplicate content)."
            ),
            expected_output=f"Single, complete customer support response written in {customer.language}",
            agent=self.us_agent
        )
        
        # Execute final response task individually
        crew_response = Crew(
            agents=[self.us_agent],
            tasks=[response_task],
            process=Process.sequential, 
            verbose=False,
            memory=False
        )
        
        print(f"🚀 Executing final response generation...")
        final_response = crew_response.kickoff()
        print(f"✅ Final response completed!")
        
        # Step 7: Completion
        yield {
            "type": "step",
            "step": {
                "agent": "US",
                "message": f"🎯 Multi-agent collaboration completed. Final response generated in {customer.language} with {customer.region} compliance.",
                "timestamp": datetime.now().isoformat(),
                "data": {"customer_data": asdict(customer), "resolution_path": f"{query.category}_tier_{customer.tier.lower()}"}
            }
        }
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Final result
        yield {
            "type": "complete",
            "collaboration": {
                "id": f"stream-collab-{int(datetime.now().timestamp())}",
                "query_id": query.id,
                "final_response": str(final_response),
                "processing_time": processing_time
            }
        }
    
    def generate_enhanced_personalized_response(self, query: SupportQuery, customer: Customer, collaboration_steps: List[AgentResponse]) -> str:
        """Generate enhanced personalized response with multi-agent context and full multi-language support."""
        # Multi-language templates
        lang_templates = {
            "German": {
                "greeting": "Guten Tag",
                "thank_you": "Vielen Dank für Ihre Kontaktaufnahme mit unserem Global Customer Support Team.",
                "processed_through": "Ihre Anfrage wurde durch unser fortschrittliches Multi-Region-Kollaborationssystem bearbeitet",
                "including_specialists": ", einschließlich unserer EU-Compliance-Spezialisten",
                "technical_analysis": "Unsere technische Analyse zeigt, dass Sie Probleme mit Ihrem {product} haben. Als geschätzter {tier}-Tier-Kunde wurde dies an unser Spezialistenteam eskaliert, das Sie innerhalb von 2 Stunden über {channel} kontaktieren wird.",
                "billing_inquiry": "Bezüglich Ihrer Rechnungsanfrage für {product} werden unsere Rechnungsspezialisten (koordiniert zwischen unseren US- und EU-Teams) Ihr Konto überprüfen und Sie über {channel} kontaktieren.",
                "general_inquiry": "Ihre allgemeine Anfrage wurde von unserem Multi-Regional-Support-Team gründlich überprüft. Basierend auf Ihrem {tier}-Tier-Status und Ihrer Service-Historie werden wir umfassende Unterstützung bieten.",
                "gdpr_notice": "🔒 Datenschutzhinweis: Diese Antwort wurde in vollständiger Übereinstimmung mit der DSGVO verarbeitet. Ihre Daten wurden ausschließlich von unseren EU-basierten Systemen und Agenten behandelt.",
                "security_notice": "🔐 Sicherheitshinweis: Ihre Anfrage wurde durch unsere sichere Multi-Regional-Infrastruktur mit angemessenen Datenschutzmaßnahmen verarbeitet.",
                "collaboration_footer": "Diese Antwort wurde durch die Zusammenarbeit zwischen unseren US- und EU-Support-Teams erstellt, um sicherzustellen, dass Sie die höchste Servicequalität in allen Regionen erhalten.",
                "best_regards": "Mit freundlichen Grüßen,\nGlobal Customer Support Team",
                "footer": "🇺🇸 US-Betrieb • 🇪🇺 EU-Compliance • 🌍 Multi-Regionale Exzellenz"
            },
            "Italian": {
                "greeting": "Buongiorno",
                "thank_you": "Grazie per aver contattato il nostro team di Global Customer Support.",
                "processed_through": "La vostra richiesta è stata elaborata attraverso il nostro avanzato sistema di collaborazione multi-regionale",
                "including_specialists": ", inclusi i nostri specialisti di conformità UE",
                "technical_analysis": "La nostra analisi tecnica indica che state riscontrando problemi con il vostro {product}. Come stimato cliente tier {tier}, questo è stato escalato al nostro team specialistico che vi contatterà tramite {channel} entro 2 ore.",
                "billing_inquiry": "Riguardo alla vostra richiesta di fatturazione per {product}, i nostri specialisti di fatturazione (coordinandosi tra i team US e UE) esamineranno il vostro account e vi contatteranno tramite {channel}.",
                "general_inquiry": "La vostra richiesta generale è stata accuratamente esaminata dal nostro team di supporto multi-regionale. Basandoci sul vostro status tier {tier} e sulla cronologia dei servizi, forniremo assistenza completa.",
                "gdpr_notice": "🔒 Avviso Protezione Dati: Questa risposta è stata elaborata in piena conformità con il regolamento GDPR. I vostri dati sono stati gestiti esclusivamente dai nostri sistemi e agenti basati nell'UE.",
                "security_notice": "🔐 Avviso Sicurezza: La vostra richiesta è stata elaborata attraverso la nostra infrastruttura multi-regionale sicura con appropriate misure di protezione dati.",
                "collaboration_footer": "Questa risposta è stata generata attraverso la collaborazione tra i nostri team di supporto US e UE, assicurando che riceviate la massima qualità del servizio in tutte le regioni.",
                "best_regards": "Cordiali saluti,\nTeam Global Customer Support",
                "footer": "🇺🇸 Operazioni US • 🇪🇺 Conformità UE • 🌍 Eccellenza Multi-Regionale"
            },
            "French": {
                "greeting": "Bonjour",
                "thank_you": "Merci d'avoir contacté notre équipe de Global Customer Support.",
                "processed_through": "Votre demande a été traitée par notre système avancé de collaboration multi-régionale",
                "including_specialists": ", incluant nos spécialistes de conformité UE",
                "technical_analysis": "Notre analyse technique indique que vous rencontrez des problèmes avec votre {product}. En tant que client estimé de niveau {tier}, ceci a été escaladé à notre équipe spécialisée qui vous contactera via {channel} dans les 2 heures.",
                "billing_inquiry": "Concernant votre demande de facturation pour {product}, nos spécialistes de facturation (coordonnant entre nos équipes US et UE) examineront votre compte et vous contacteront via {channel}.",
                "general_inquiry": "Votre demande générale a été soigneusement examinée par notre équipe de support multi-régionale. Basé sur votre statut niveau {tier} et l'historique de service, nous fournirons une assistance complète.",
                "gdpr_notice": "🔒 Avis Protection des Données: Cette réponse a été traitée en pleine conformité avec le règlement RGPD. Vos données ont été gérées exclusivement par nos systèmes et agents basés dans l'UE.",
                "security_notice": "🔐 Avis Sécurité: Votre demande a été traitée par notre infrastructure multi-régionale sécurisée avec des mesures appropriées de protection des données.",
                "collaboration_footer": "Cette réponse a été générée par la collaboration entre nos équipes de support US et UE, garantissant que vous recevez la plus haute qualité de service dans toutes les régions.",
                "best_regards": "Cordialement,\nÉquipe Global Customer Support",
                "footer": "🇺🇸 Opérations US • 🇪🇺 Conformité UE • 🌍 Excellence Multi-Régionale"
            },
            "English": {
                "greeting": "Hello",
                "thank_you": "Thank you for contacting our Global Customer Support team.",
                "processed_through": "Your inquiry has been processed through our advanced multi-region collaboration system",
                "including_specialists": ", including our EU compliance specialists",
                "technical_analysis": "Our technical analysis indicates you're experiencing issues with your {product}. As a valued {tier} tier customer, this has been escalated to our specialist team who will contact you via {channel} within 2 hours.",
                "billing_inquiry": "Regarding your billing inquiry for {product}, our billing specialists (coordinating between our US and EU teams) will review your account and contact you via {channel}.",
                "general_inquiry": "Your general inquiry has been thoroughly reviewed by our multi-regional support team. Based on your {tier} tier status and service history, we'll provide comprehensive assistance.",
                "gdpr_notice": "🔒 Data Protection Notice: This response was processed in full compliance with GDPR regulations. Your data was handled exclusively by our EU-based systems and agents.",
                "security_notice": "🔐 Security Notice: Your inquiry was processed through our secure multi-regional infrastructure with appropriate data protection measures.",
                "collaboration_footer": "This response was generated through collaboration between our US and EU support teams, ensuring you receive the highest quality of service across all regions.",
                "best_regards": "Best regards,\nGlobal Customer Support Team",
                "footer": "🇺🇸 US Operations • 🇪🇺 EU Compliance • 🌍 Multi-Regional Excellence"
            }
        }
        
        # Get language template (fallback to English)
        lang = lang_templates.get(customer.language, lang_templates["English"])
        greeting = lang["greeting"]
        
        response = f"{greeting} {customer.name},\n\n"
        
        # Add collaboration context with language support
        response += lang["thank_you"] + " " + lang["processed_through"]
        if any(step.agent == "EU" for step in collaboration_steps):
            response += lang["including_specialists"]
        response += ".\n\n"
        
        # Category-specific response with multi-language support
        product = customer.purchases[-1].product if customer.purchases else 'current setup'
        
        if query.category == "technical":
            response += lang["technical_analysis"].format(
                product=product,
                tier=customer.tier,
                channel=customer.preferred_channel
            ) + "\n\n"
        
        elif query.category == "billing":
            response += lang["billing_inquiry"].format(
                product=product,
                channel=customer.preferred_channel
            ) + "\n\n"
            
        elif query.category == "general":
            response += lang["general_inquiry"].format(tier=customer.tier) + "\n\n"
        
        # Regional compliance note with language support
        if customer.region == "EU":
            response += lang["gdpr_notice"] + "\n\n"
        else:
            response += lang["security_notice"] + "\n\n"
        
        # Multi-language collaboration footer
        response += lang["collaboration_footer"] + "\n\n"
        response += lang["best_regards"] + "\n"
        response += lang["footer"]
        
        return response


def demo_customer_support():
    """Demo function to test the customer support system."""
    service = GlobalCustomerSupportService()
    
    # Sample queries
    sample_queries = [
        SupportQuery(
            id="q1",
            customer_id="cust-us-001",
            message="I'm having trouble with the new compliance module. It keeps showing false positives for our internal communications.",
            timestamp=datetime.now().isoformat(),
            priority="high",
            category="technical"
        ),
        SupportQuery(
            id="q2",
            customer_id="cust-eu-001",
            message="I need to understand how your threat detection system handles GDPR data processing requirements.",
            timestamp=datetime.now().isoformat(),
            priority="medium",
            category="general"
        )
    ]
    
    print("🌍 Global Customer Support Demo Starting...")
    print("=" * 60)
    
    for query in sample_queries:
        customer = CustomerService.get_customer_by_id(query.customer_id)
        print(f"\n📋 Processing Query from {customer.name} ({customer.region})")
        print(f"Query: {query.message}")
        print("-" * 60)
        
        collaboration = service.process_query(query)
        
        print("\n🤝 Agent Collaboration Steps:")
        for i, step in enumerate(collaboration.steps, 1):
            print(f"{i}. [{step.agent} Agent] {step.message}")
        
        print(f"\n💬 Final Response ({collaboration.processing_time}ms):")
        print(collaboration.final_response)
        print("=" * 60)


if __name__ == "__main__":
    demo_customer_support()