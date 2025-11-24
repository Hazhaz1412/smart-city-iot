from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ngsi_ld import NGSILDContext
from .orion_client import OrionLDClient
import logging

logger = logging.getLogger(__name__)


class ContextView(APIView):
    """API endpoint to serve the JSON-LD @context"""
    
    def get(self, request):
        """Return the JSON-LD context"""
        return Response(NGSILDContext.get_context_dict())


class HealthCheckView(APIView):
    """Health check endpoint"""
    
    def get(self, request):
        """Check system health"""
        health_status = {
            "status": "healthy",
            "services": {}
        }
        
        # Check Orion-LD
        try:
            client = OrionLDClient()
            response = client.query_entities(limit=1)
            health_status["services"]["orion_ld"] = "healthy"
        except Exception as e:
            logger.error(f"Orion-LD health check failed: {e}")
            health_status["services"]["orion_ld"] = "unhealthy"
            health_status["status"] = "degraded"
        
        return Response(health_status)
