"""
Orion-LD Context Broker client
"""
import requests
from typing import Dict, Any, List, Optional
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class OrionLDClient:
    """Client for interacting with Orion-LD Context Broker"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.ORION_LD_URL
        self.headers = {
            "Content-Type": "application/ld+json",
            "Accept": "application/ld+json"
        }
    
    def create_entity(self, entity: Dict[str, Any]) -> bool:
        """Create a new entity in Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/entities"
        
        try:
            response = requests.post(url, json=entity, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Created entity: {entity.get('id')}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create entity: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get an entity from Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/entities/{entity_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get entity {entity_id}: {e}")
            return None
    
    def update_entity(
        self,
        entity_id: str,
        attributes: Dict[str, Any]
    ) -> bool:
        """Update entity attributes"""
        url = f"{self.base_url}/ngsi-ld/v1/entities/{entity_id}/attrs"
        
        try:
            response = requests.patch(url, json=attributes, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Updated entity: {entity_id}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update entity {entity_id}: {e}")
            return False
    
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity from Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/entities/{entity_id}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Deleted entity: {entity_id}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete entity {entity_id}: {e}")
            return False
    
    def query_entities(
        self,
        entity_type: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        georel: Optional[str] = None,
        geometry: Optional[str] = None,
        coordinates: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query entities from Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/entities"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if entity_type:
            params["type"] = entity_type
        
        if q:
            params["q"] = q
        
        if georel and geometry and coordinates:
            params["georel"] = georel
            params["geometry"] = geometry
            params["coordinates"] = coordinates
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to query entities: {e}")
            return []
    
    def create_subscription(self, subscription: Dict[str, Any]) -> Optional[str]:
        """Create a subscription in Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/subscriptions"
        
        try:
            response = requests.post(url, json=subscription, headers=self.headers)
            response.raise_for_status()
            
            # Get subscription ID from Location header
            location = response.headers.get('Location', '')
            subscription_id = location.split('/')[-1] if location else None
            
            logger.info(f"Created subscription: {subscription_id}")
            return subscription_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create subscription: {e}")
            return None
    
    def get_subscription(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """Get a subscription from Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/subscriptions/{subscription_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get subscription {subscription_id}: {e}")
            return None
    
    def delete_subscription(self, subscription_id: str) -> bool:
        """Delete a subscription from Orion-LD"""
        url = f"{self.base_url}/ngsi-ld/v1/subscriptions/{subscription_id}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Deleted subscription: {subscription_id}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete subscription {subscription_id}: {e}")
            return False
    
    def get_temporal_entities(
        self,
        entity_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        time_rel: str = "between",
        time_at: Optional[str] = None,
        end_time_at: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Query temporal entities"""
        url = f"{self.base_url}/ngsi-ld/v1/temporal/entities"
        
        params = {
            "timerel": time_rel,
            "limit": limit
        }
        
        if entity_id:
            params["id"] = entity_id
        
        if entity_type:
            params["type"] = entity_type
        
        if time_at:
            params["timeAt"] = time_at
        
        if end_time_at:
            params["endTimeAt"] = end_time_at
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to query temporal entities: {e}")
            return []
