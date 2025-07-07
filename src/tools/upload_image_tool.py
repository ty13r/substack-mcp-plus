# ABOUTME: MCP tool class for uploading images to Substack CDN
# ABOUTME: Supports file paths, URLs, and returns optimized CDN URLs

from typing import Dict, Any, Optional, Literal
from src.handlers.image_handler import ImageHandler


class UploadImageTool:
    """Tool for uploading images to Substack CDN"""
    
    def __init__(self, server):
        """Initialize the tool with server reference"""
        self.server = server
        self.name = "upload_image"
        self.description = "Upload an image to Substack CDN and get an optimized URL."
        self.input_schema = {
            "type": "object",
            "required": ["source"],
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Image source - can be a file path or URL"
                },
                "optimize_for": {
                    "type": "string",
                    "enum": ["web", "email", "thumbnail"],
                    "default": "web",
                    "description": "Optimization preset: web (1456px), email (600px), or thumbnail (300px)"
                },
                "caption": {
                    "type": "string",
                    "description": "Optional caption for the image"
                }
            }
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        source = arguments.get("source")
        optimize_for = arguments.get("optimize_for", "web")
        caption = arguments.get("caption")
        
        if not source:
            raise ValueError("source is required")
        
        try:
            # Create image handler with authenticated client
            image_handler = ImageHandler(self.server.post_handler.client)
            
            # Upload the image
            result = await image_handler.upload_image(source)
            
            # Get optimized URL based on use case
            optimization_params = {
                "web": {"width": 1456, "quality": "auto:good"},
                "email": {"width": 600, "quality": "auto:good"},
                "thumbnail": {"width": 300, "quality": "auto:low"}
            }
            
            params = optimization_params.get(optimize_for, optimization_params["web"])
            optimized_url = image_handler.get_optimized_url(
                result["url"],
                width=params["width"],
                quality=params["quality"]
            )
            
            return {
                "success": True,
                "url": optimized_url,
                "original_url": result["url"],
                "id": result["id"],
                "filename": result.get("filename"),
                "caption": caption,
                "optimization": optimize_for,
                "message": f"Image uploaded successfully and optimized for {optimize_for}"
            }
            
        except FileNotFoundError as e:
            return {
                "success": False,
                "error": f"File not found: {str(e)}"
            }
        except ValueError as e:
            return {
                "success": False,
                "error": f"Invalid image: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Upload failed: {str(e)}"
            }