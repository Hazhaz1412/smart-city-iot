"""
Custom JSON-LD renderer for REST Framework
"""
from rest_framework.renderers import JSONRenderer


class JSONLDRenderer(JSONRenderer):
    """Renderer for JSON-LD content"""
    
    media_type = 'application/ld+json'
    format = 'jsonld'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render data as JSON-LD"""
        return super().render(data, accepted_media_type, renderer_context)
