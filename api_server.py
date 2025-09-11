#!/usr/bin/env python3
"""
Flask API Server for Global Customer Support Demo
Provides REST endpoints for React frontend integration.
"""

import json
from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dataclasses import asdict
from customer_support import (
    GlobalCustomerSupportService,
    CustomerService,
    SupportQuery,
    CollaborationLog
)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize the customer support service
support_service = GlobalCustomerSupportService()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'us_agent': 'active',
            'eu_agent': 'active'
        }
    })


@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers."""
    region = request.args.get('region')
    
    if region:
        customers = CustomerService.get_customers_by_region(region.upper())
    else:
        customers = CustomerService.CUSTOMERS
    
    return jsonify({
        'customers': [asdict(customer) for customer in customers],
        'count': len(customers)
    })


@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a specific customer by ID."""
    customer = CustomerService.get_customer_by_id(customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    return jsonify({'customer': asdict(customer)})


@app.route('/api/support/query', methods=['POST'])
def submit_support_query():
    """Submit a customer support query with real-time step-by-step processing."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_id', 'message', 'category', 'priority']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create support query
        query = SupportQuery(
            id=f"q-{int(datetime.now().timestamp())}",
            customer_id=data['customer_id'],
            message=data['message'],
            timestamp=datetime.now().isoformat(),
            priority=data['priority'],
            category=data['category']
        )
        
        # Use real LLM processing with actual agent collaboration
        collaboration = support_service.process_query(query)
        
        # Convert to dict for JSON response
        result = {
            'collaboration': {
                'id': collaboration.id,
                'query_id': collaboration.query_id,
                'steps': [asdict(step) for step in collaboration.steps],
                'final_response': collaboration.final_response,
                'processing_time': collaboration.processing_time
            },
            'query': asdict(query),
            'customer': asdict(CustomerService.get_customer_by_id(query.customer_id))
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/support/query-stream', methods=['POST'])
def submit_support_query_stream():
    """Submit a support query with real-time streaming updates."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_id', 'message', 'category', 'priority']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create support query
        query = SupportQuery(
            id=f"q-{int(datetime.now().timestamp())}",
            customer_id=data['customer_id'],
            message=data['message'],
            timestamp=datetime.now().isoformat(),
            priority=data['priority'],
            category=data['category']
        )
        
        def generate_steps():
            """Generator function for streaming collaboration steps."""
            for step_data in support_service.process_query_stream(query):
                yield f"data: {json.dumps(step_data)}\n\n"
        
        return Response(
            generate_steps(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/support/sample-queries', methods=['GET'])
def get_sample_queries():
    """Get sample support queries for testing."""
    sample_queries = [
        {
            'id': 'q1',
            'customer_id': 'cust-us-001',
            'message': "I'm having trouble with the new compliance module. It keeps showing false positives for our internal communications.",
            'priority': 'high',
            'category': 'technical'
        },
        {
            'id': 'q2',
            'customer_id': 'cust-eu-001',
            'message': "I need to understand how your threat detection system handles GDPR data processing requirements.",
            'priority': 'medium',
            'category': 'general'
        },
        {
            'id': 'q3',
            'customer_id': 'cust-eu-002',
            'message': "Can I get a refund for the security package? It doesn't meet our current needs.",
            'priority': 'high',
            'category': 'billing'
        },
        {
            'id': 'q4',
            'customer_id': 'cust-us-002',
            'message': "How do I upgrade from Bronze to Silver tier? What are the additional features?",
            'priority': 'low',
            'category': 'general'
        },
        {
            'id': 'q5',
            'customer_id': 'cust-eu-003',
            'message': "Guten Tag, ich habe Probleme mit der neuen Analytics-Module. Die Berichte werden nicht korrekt generiert und zeigen falsche Metriken an. Können Sie mir bei der Konfiguration helfen?",
            'priority': 'high',
            'category': 'technical'
        },
        {
            'id': 'q6',
            'customer_id': 'cust-eu-004',
            'message': "Buongiorno, vorrei sapere come posso aggiornare il mio piano attuale per includere funzionalità di compliance avanzate. Il nostro team ha bisogno di maggiori strumenti di reporting per conformità normative.",
            'priority': 'medium',
            'category': 'general'
        }
    ]
    
    # Add customer info to each query
    enriched_queries = []
    for query in sample_queries:
        customer = CustomerService.get_customer_by_id(query['customer_id'])
        enriched_queries.append({
            **query,
            'customer': asdict(customer) if customer else None,
            'timestamp': datetime.now().isoformat()
        })
    
    return jsonify({'queries': enriched_queries})


@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Get status of all agents."""
    return jsonify({
        'agents': {
            'us_agent': {
                'role': support_service.us_agent.role,
                'endpoint': 'http://20.185.179.136:61100/v1',
                'status': 'active',
                'region': 'US'
            },
            'eu_agent': {
                'role': support_service.eu_agent.role,
                'endpoint': 'http://9.163.149.120:61102/v1',
                'status': 'active',
                'region': 'EU'
            }
        },
        'collaboration_flow': [
            'US Agent analyzes incoming query',
            'EU Agent handles GDPR-compliant data access (if EU customer)',
            'US Agent generates personalized response using all available context'
        ]
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting Global Customer Support API Server...")
    print("🇺🇸 US Agent: http://20.185.179.136:61100/v1")
    print("🇪🇺 EU Agent: http://9.163.149.120:61102/v1")
    print("🌐 API Server: http://localhost:5001")
    print("-" * 50)
    
    app.run(
        host='0.0.0.0',
        port=5001,  # Changed from 5000 to avoid conflicts
        debug=True,
        threaded=True
    )