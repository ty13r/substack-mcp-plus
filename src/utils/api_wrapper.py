# ABOUTME: API wrapper to handle python-substack string error responses
# ABOUTME: Provides consistent error handling for all API calls

import logging
from typing import Any, Dict, List, Optional, Union, Callable
from functools import wraps

logger = logging.getLogger(__name__)


class SubstackAPIError(Exception):
    """Custom exception for Substack API errors"""
    pass


class APIWrapper:
    """Wrapper for python-substack API client to handle string errors"""
    
    def __init__(self, client):
        """Initialize wrapper with the underlying client
        
        Args:
            client: The python-substack API client
        """
        self.client = client
        self.publication_url = client.publication_url
        
        # Debug logging
        logger.debug(f"APIWrapper initialized with client type: {type(client)}")
        logger.debug(f"Client has get_draft method: {hasattr(client, 'get_draft')}")
    
    def _handle_response(self, response: Any, method_name: str) -> Any:
        """Handle API response and convert errors to exceptions
        
        Args:
            response: The API response
            method_name: Name of the method called (for error messages)
            
        Returns:
            The response if valid
            
        Raises:
            SubstackAPIError: If response is an error
        """
        # Check for None responses
        if response is None:
            raise SubstackAPIError(f"{method_name} returned None")
        
        # Check for string responses (always errors)
        if isinstance(response, str):
            # Log the string error
            logger.error(f"{method_name} returned string: {response}")
            
            # Parse common error patterns
            if "not found" in response.lower():
                raise SubstackAPIError(f"Post not found")
            elif "unauthorized" in response.lower() or "authentication" in response.lower():
                raise SubstackAPIError(f"Authentication failed - please check your credentials")
            elif "rate limit" in response.lower():
                raise SubstackAPIError(f"Rate limit exceeded - please try again later")
            else:
                # Generic error for any other string response
                raise SubstackAPIError(f"API error: {response}")
        
        # Check for error objects (dict with 'error' key)
        if isinstance(response, dict) and 'error' in response:
            error_msg = response.get('error', 'Unknown error')
            logger.error(f"{method_name} returned error object: {error_msg}")
            
            # Parse the error message
            if isinstance(error_msg, str):
                if "not found" in error_msg.lower():
                    raise SubstackAPIError(f"Post not found")
                elif "unauthorized" in error_msg.lower():
                    raise SubstackAPIError(f"Authentication failed")
                else:
                    raise SubstackAPIError(f"API error: {error_msg}")
            else:
                raise SubstackAPIError(f"API error: {response}")
        
        return response
    
    def get_user_id(self) -> str:
        """Get user ID with error handling"""
        try:
            result = self.client.get_user_id()
            # User ID is expected to be a string, so don't use _handle_response
            if result is None:
                raise SubstackAPIError("get_user_id returned None")
            return str(result)
        except AttributeError:
            # Method might not exist
            raise SubstackAPIError("get_user_id method not available")
    
    def get_draft(self, post_id: str) -> Dict[str, Any]:
        """Get a draft with error handling"""
        try:
            logger.debug(f"APIWrapper.get_draft called with post_id: {post_id}")
            logger.debug(f"About to call self.client.get_draft, client type: {type(self.client)}")
            
            result = self.client.get_draft(post_id)
            # Log what we got back
            logger.debug(f"get_draft({post_id}) returned type: {type(result)}")
            if isinstance(result, str):
                logger.debug(f"get_draft returned string: {result}")
            
            # Handle the response
            checked_result = self._handle_response(result, "get_draft")
            
            # Additional validation for draft structure
            if not isinstance(checked_result, dict):
                raise SubstackAPIError(f"Invalid draft response - expected dict, got {type(checked_result)}")
            
            # Ensure it has at least some expected fields
            # Don't require all fields as draft structure may vary
            if not any(key in checked_result for key in ['id', 'draft_title', 'title', 'body', 'draft_body']):
                logger.warning(f"Draft response missing expected fields. Keys: {list(checked_result.keys())[:10]}")
            
            return checked_result
            
        except SubstackAPIError:
            # Let our own errors bubble up
            raise
        except KeyError as e:
            # Handle KeyError from python-substack
            key_name = str(e).strip("'")
            raise SubstackAPIError(f"Missing required field in API response: {key_name}")
        except AttributeError as e:
            # Handle AttributeError (e.g., 'str' object has no attribute 'get')
            logger.error(f"AttributeError in APIWrapper.get_draft: {str(e)}")
            logger.error(f"Full exception details: {repr(e)}")
            raise SubstackAPIError(f"Invalid API response format: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected exception in get_draft: {type(e).__name__}: {str(e)}")
            raise SubstackAPIError(f"Failed to get post {post_id}: {str(e)}")
    
    def get_drafts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get drafts with error handling"""
        try:
            result = self.client.get_drafts(limit=limit)
            # Convert generator to list and check each item
            drafts = []
            for draft in result:
                checked_draft = self._handle_response(draft, "get_drafts[item]")
                if isinstance(checked_draft, dict):
                    drafts.append(checked_draft)
            return drafts
        except Exception as e:
            logger.error(f"get_drafts error: {str(e)}")
            return []
    
    def post_draft(self, draft_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a draft with error handling"""
        try:
            result = self.client.post_draft(draft_data)
            return self._handle_response(result, "post_draft")
        except Exception as e:
            raise SubstackAPIError(f"Failed to create draft: {str(e)}")
    
    def put_draft(self, post_id: str, **kwargs) -> Dict[str, Any]:
        """Update a draft with error handling"""
        try:
            result = self.client.put_draft(post_id, **kwargs)
            return self._handle_response(result, "put_draft")
        except Exception as e:
            raise SubstackAPIError(f"Failed to update draft: {str(e)}")
    
    def publish_draft(self, post_id: str) -> Dict[str, Any]:
        """Publish a draft with error handling"""
        try:
            result = self.client.publish_draft(post_id)
            return self._handle_response(result, "publish_draft")
        except Exception as e:
            raise SubstackAPIError(f"Failed to publish draft: {str(e)}")
    
    def delete_draft(self, post_id: str) -> bool:
        """Delete a draft with error handling"""
        try:
            result = self.client.delete_draft(post_id)
            if isinstance(result, str):
                if "deleted" in result.lower() or "success" in result.lower():
                    return True
                else:
                    raise SubstackAPIError(f"Delete failed: {result}")
            return True
        except Exception as e:
            raise SubstackAPIError(f"Failed to delete draft: {str(e)}")
    
    def schedule_draft(self, post_id: str, scheduled_at) -> Dict[str, Any]:
        """Schedule a draft with error handling"""
        try:
            result = self.client.schedule_draft(post_id, scheduled_at)
            return self._handle_response(result, "schedule_draft")
        except Exception as e:
            raise SubstackAPIError(f"Failed to schedule draft: {str(e)}")
    
    def unschedule_draft(self, post_id: str) -> Dict[str, Any]:
        """Unschedule a draft with error handling"""
        try:
            result = self.client.unschedule_draft(post_id)
            return self._handle_response(result, "unschedule_draft")
        except Exception as e:
            raise SubstackAPIError(f"Failed to unschedule draft: {str(e)}")
    
    def prepublish_draft(self, post_id: str) -> Dict[str, Any]:
        """Prepublish a draft with error handling"""
        try:
            result = self.client.prepublish_draft(post_id)
            return self._handle_response(result, "prepublish_draft")
        except Exception as e:
            # This method might not exist or might fail silently
            logger.warning(f"prepublish_draft failed: {str(e)}")
            return {}
    
    def get_sections(self) -> List[Dict[str, Any]]:
        """Get sections with error handling"""
        try:
            result = self.client.get_sections()
            if result is None:
                return []
            # Convert generator to list
            sections = []
            for section in result:
                checked_section = self._handle_response(section, "get_sections[item]")
                if isinstance(checked_section, dict):
                    sections.append(checked_section)
            return sections
        except Exception as e:
            logger.error(f"get_sections error: {str(e)}")
            return []
    
    def get_publication_subscriber_count(self) -> int:
        """Get subscriber count with error handling"""
        try:
            # The python-substack method directly accesses ["subscriberCount"]
            # which will raise KeyError if the key doesn't exist
            result = self.client.get_publication_subscriber_count()
            
            # If we get here, the library successfully extracted the count
            if isinstance(result, (int, float)):
                return int(result)
            else:
                raise SubstackAPIError(f"Unexpected subscriber count type: {type(result)}")
                
        except KeyError as e:
            # This happens when the API response doesn't have 'subscriberCount' key
            logger.warning(f"subscriberCount key not found in API response: {e}")
            
            # Try alternative via sections
            try:
                sections = self.get_sections()
                if sections:
                    # Sum up subscriber counts from sections
                    total = 0
                    for section in sections:
                        total += section.get('subscriber_count', 0)
                    if total > 0:
                        logger.info(f"Got subscriber count from sections: {total}")
                        return total
                
                # If no sections or no counts, raise error
                raise SubstackAPIError("Unable to get subscriber count - no data available")
                
            except Exception as e2:
                logger.error(f"Failed to get subscriber count from sections: {e2}")
                raise SubstackAPIError("Unable to get subscriber count from publication or sections")
                
        except AttributeError as e:
            # Method might not exist or client might be None
            raise SubstackAPIError(f"API client error: {str(e)}")
            
        except Exception as e:
            # Any other unexpected error
            logger.error(f"Unexpected error getting subscriber count: {type(e).__name__}: {str(e)}")
            raise SubstackAPIError(f"Failed to get subscriber count: {str(e)}")