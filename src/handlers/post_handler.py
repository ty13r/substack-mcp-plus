# ABOUTME: PostHandler class for managing Substack post operations
# ABOUTME: Handles creating, updating, publishing, and listing posts with formatting

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging
from src.converters.markdown_converter import MarkdownConverter
from src.converters.html_converter import HTMLConverter
from src.converters.block_builder import BlockBuilder
from src.utils.api_wrapper import SubstackAPIError
from substack.post import Post

logger = logging.getLogger(__name__)


class PostHandler:
    """Handles post operations for Substack"""

    def __init__(self, client):
        """Initialize the post handler with an authenticated client

        Args:
            client: An authenticated Substack API client
        """
        self.client = client
        self.markdown_converter = MarkdownConverter()
        self.html_converter = HTMLConverter()
        self.block_builder = BlockBuilder()

        # Debug: Log client type and attributes
        logger.debug(f"PostHandler initialized with client type: {type(client)}")
        logger.debug(f"Client class name: {client.__class__.__name__}")
        logger.debug(
            f"Client has _handle_response: {hasattr(client, '_handle_response')}"
        )
        logger.debug(
            f"Client attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}[:10]"
        )

    async def create_draft(
        self,
        title: str,
        content: str,
        subtitle: Optional[str] = None,
        content_type: str = "markdown",
    ) -> Dict[str, Any]:
        """Create a draft post with formatted content

        Args:
            title: The post title
            content: The post content (markdown, HTML, or plain text)
            subtitle: Optional subtitle for the post
            content_type: Type of content ("markdown", "html", or "plain")

        Returns:
            The created post data from Substack

        Raises:
            ValueError: If content_type is not supported or invalid input
        """
        # Input validation
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")

        if len(title) > 280:  # Substack title limit
            raise ValueError("Title must be 280 characters or less")

        if not content or not isinstance(content, str):
            raise ValueError("Content must be a non-empty string")

        if subtitle is not None and not isinstance(subtitle, str):
            raise ValueError("Subtitle must be a string if provided")

        if subtitle and len(subtitle) > 280:  # Substack subtitle limit
            raise ValueError("Subtitle must be 280 characters or less")

        valid_content_types = ["markdown", "html", "plain"]
        if content_type not in valid_content_types:
            raise ValueError(
                f"content_type must be one of: {', '.join(valid_content_types)}"
            )
        # Convert content to blocks based on type
        blocks = self._convert_content_to_blocks(content, content_type)

        # Handle paywall markers in content
        blocks = self._process_paywall_markers(content, blocks, content_type)

        # Remove duplicate title if the first block is a heading matching the post title
        if blocks and blocks[0].get("type") in [
            "heading-one",
            "heading-two",
            "heading-three",
            "heading-four",
            "heading-five",
            "heading-six",
        ]:
            # Extract text from the first block's content
            first_block_text = self._extract_text_from_content(
                blocks[0].get("content", [])
            )
            # Compare case-insensitively
            if first_block_text.strip().lower() == title.strip().lower():
                logger.info(
                    f"Removing duplicate title from content: {first_block_text}"
                )
                blocks = blocks[1:]  # Skip the first block

        # Format blocks for API
        body = self._format_blocks_for_api(blocks)

        # Create a Post object as required by python-substack
        # Get user_id from the client
        user_id = self.client.get_user_id()

        # Check if content has paywall markers - if so, set audience to paid subscribers
        audience = "everyone"  # default
        paywall_markers = [
            "<!-- PAYWALL -->",
            "<!--PAYWALL-->",
            "<!--paywall-->",
            "<!-- paywall -->",
        ]
        if content_type == "markdown":
            for marker in paywall_markers:
                if marker in content:
                    audience = "only_paid"
                    break

        # Create Post object
        post = Post(
            title=title, subtitle=subtitle or "", user_id=user_id, audience=audience
        )

        # Add content blocks using the Post object's methods
        self._add_blocks_to_post(post, blocks)

        # Create the draft
        return self.client.post_draft(post.get_draft())

    async def update_draft(
        self,
        post_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        subtitle: Optional[str] = None,
        content_type: str = "markdown",
    ) -> Dict[str, Any]:
        """Update an existing draft post

        Args:
            post_id: The ID of the post to update
            title: New title (optional)
            content: New content (optional)
            subtitle: New subtitle (optional)
            content_type: Type of content if content is provided

        Returns:
            The updated post data from Substack

        Raises:
            ValueError: If invalid input provided
        """
        # Input validation
        if not post_id or not isinstance(post_id, str):
            raise ValueError("post_id must be a non-empty string")

        if title is not None:
            if not isinstance(title, str) or not title:
                raise ValueError("Title must be a non-empty string if provided")
            if len(title) > 280:
                raise ValueError("Title must be 280 characters or less")

        if subtitle is not None:
            if not isinstance(subtitle, str):
                raise ValueError("Subtitle must be a string if provided")
            if len(subtitle) > 280:
                raise ValueError("Subtitle must be 280 characters or less")

        if content is not None:
            if not isinstance(content, str) or not content:
                raise ValueError("Content must be a non-empty string if provided")

            valid_content_types = ["markdown", "html", "plain"]
            if content_type not in valid_content_types:
                raise ValueError(
                    f"content_type must be one of: {', '.join(valid_content_types)}"
                )
        # Get the current draft to check if it's published
        current_draft = self.client.get_draft(post_id)
        is_draft = not current_draft.get("post_date")

        update_data = {}

        if title is not None:
            # Use draft_title for drafts, title for published
            if is_draft:
                update_data["draft_title"] = title
            else:
                update_data["title"] = title

        if subtitle is not None:
            # Use draft_subtitle for drafts, subtitle for published
            if is_draft:
                update_data["draft_subtitle"] = subtitle
            else:
                update_data["subtitle"] = subtitle

        if content is not None:
            # For content updates, we need to use the same format as Post.get_draft()
            # Create a temporary Post object to format the content properly
            temp_post = Post(
                title=title or "Temp",
                subtitle=subtitle or "",
                user_id=self.client.get_user_id(),
            )

            # Convert and add blocks
            blocks = self._convert_content_to_blocks(content, content_type)
            blocks = self._process_paywall_markers(content, blocks, content_type)

            # Remove duplicate title if updating with a title and first block matches
            if (
                title is not None
                and blocks
                and blocks[0].get("type")
                in [
                    "heading-one",
                    "heading-two",
                    "heading-three",
                    "heading-four",
                    "heading-five",
                    "heading-six",
                ]
            ):
                first_block_text = self._extract_text_from_content(
                    blocks[0].get("content", [])
                )
                if first_block_text.strip().lower() == title.strip().lower():
                    logger.info(
                        f"Removing duplicate title from updated content: {first_block_text}"
                    )
                    blocks = blocks[1:]

            # Add blocks to Post object
            self._add_blocks_to_post(temp_post, blocks)

            # Get the properly formatted draft data
            temp_draft = temp_post.get_draft()

            # Use draft_body for drafts, body for published
            if is_draft:
                update_data["draft_body"] = temp_draft["draft_body"]
            else:
                update_data["body"] = temp_draft["draft_body"]  # Same format for both

        return self.client.put_draft(post_id, **update_data)

    async def publish_draft(self, post_id: str) -> Dict[str, Any]:
        """Publish a draft post immediately

        Args:
            post_id: The ID of the draft to publish

        Returns:
            The published post data

        Raises:
            ValueError: If invalid input provided
        """
        # Input validation
        if not post_id or not isinstance(post_id, str):
            raise ValueError("post_id must be a non-empty string")

        return self.client.publish_draft(post_id)

    async def list_drafts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent draft posts

        Args:
            limit: Maximum number of drafts to return (1-50)

        Returns:
            List of draft posts

        Raises:
            ValueError: If limit is invalid
        """
        # Input validation
        if not isinstance(limit, int):
            raise ValueError("limit must be an integer")

        if limit < 1 or limit > 25:
            raise ValueError("limit must be between 1 and 25")
        # python-substack returns a generator, convert to list
        # The API returns all posts, so we need to filter for drafts only
        try:
            # Debug: Let's see what client we're using
            logger.info(f"Client type: {type(self.client)}")
            logger.info(f"Client class name: {self.client.__class__.__name__}")

            # Check publication info
            if hasattr(self.client, "client") and hasattr(
                self.client.client, "publication_id"
            ):
                logger.info(f"Publication ID: {self.client.client.publication_id}")
            if hasattr(self.client, "client") and hasattr(
                self.client.client, "subdomain"
            ):
                logger.info(f"Subdomain: {self.client.client.subdomain}")

            # Try to get the raw API response
            # Note: Substack API seems to have a lower limit than expected
            raw_result = self.client.get_drafts(limit=min(limit, 25))
            logger.info(f"Raw result type: {type(raw_result)}")

            all_posts = list(raw_result)
            logger.info(f"Retrieved {len(all_posts)} posts from API")

            # If empty, let's try a different approach
            if len(all_posts) == 0:
                logger.warning("get_drafts returned empty, trying direct API call")
                # Check if we have the underlying client
                if hasattr(self.client, "client"):
                    logger.info("Found underlying client, checking its properties")
                    inner_client = self.client.client
                    logger.info(f"Inner client type: {type(inner_client)}")
                    logger.info(
                        f"Inner client dir: {[x for x in dir(inner_client) if not x.startswith('_')][:10]}"
                    )
        except Exception as e:
            logger.error(f"Error getting drafts: {type(e).__name__}: {e}")
            import traceback

            logger.error(traceback.format_exc())
            return []

        drafts = []

        for post in all_posts:
            # Log the post structure for debugging
            logger.debug(f"Post keys: {list(post.keys())[:10]}")
            logger.debug(f"Post type: {post.get('type')}")
            logger.debug(f"Post has draft_title: {post.get('draft_title') is not None}")
            logger.debug(f"Post has title: {post.get('title') is not None}")
            logger.debug(f"Post has post_date: {post.get('post_date') is not None}")

            # For debugging: add ALL posts to see what we're getting
            drafts.append(post)
            if len(drafts) >= limit:
                break

        logger.info(f"Returning {len(drafts)} drafts")
        return drafts

    async def list_published(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent published posts

        Args:
            limit: Maximum number of published posts to return (1-50)

        Returns:
            List of published posts

        Raises:
            ValueError: If limit is invalid
        """
        # Input validation
        if not isinstance(limit, int):
            raise ValueError("limit must be an integer")

        if limit < 1 or limit > 25:
            raise ValueError("limit must be between 1 and 25")

        # Get all posts and filter for published only
        all_posts = self.client.get_drafts(limit=min(limit, 25))
        published = []

        for post in all_posts:
            # Check if it's published (has a post_date)
            if post.get("post_date"):
                published.append(post)
                if len(published) >= limit:
                    break

        return published

    async def get_post(self, post_id: str) -> Dict[str, Any]:
        """Get a specific post by ID

        Args:
            post_id: The ID of the post to retrieve

        Returns:
            The post data
        """
        # python-substack uses get_draft for both drafts and published posts
        return self.client.get_draft(post_id)

    async def get_post_content(self, post_id: str) -> Dict[str, Any]:
        """Get the full content of a post with formatting details

        Args:
            post_id: The ID of the post to read

        Returns:
            Post data with title, subtitle, and formatted content
        """
        try:
            # Debug logging
            logger.debug(f"get_post_content called with post_id: {post_id}")
            logger.debug(f"Client type: {type(self.client)}")
            logger.debug(f"Client class: {self.client.__class__.__name__}")
            logger.debug(
                f"Is APIWrapper: {self.client.__class__.__name__ == 'APIWrapper'}"
            )

            # This should raise SubstackAPIError if response is a string
            logger.debug(f"About to call client.get_draft({post_id})")
            post = self.client.get_draft(post_id)
            logger.debug(f"get_draft returned successfully, type: {type(post)}")

            # Extra safety check
            if not isinstance(post, dict):
                logger.error(
                    f"Unexpected response type from Substack API: {type(post)}, value: {post}"
                )
                raise ValueError(
                    f"Invalid response from Substack API - expected dict, got {type(post)}"
                )

            # Debug: Log the structure of the response
            logger.debug(f"Post keys: {list(post.keys())[:20]}")
            logger.debug(
                f"Has body: {'body' in post}, Has draft_body: {'draft_body' in post}"
            )
            if "body" in post:
                logger.debug(f"body type: {type(post['body'])}")
                if isinstance(post["body"], dict):
                    logger.debug(f"body keys: {list(post['body'].keys())[:10]}")
            if "draft_body" in post:
                logger.debug(f"draft_body type: {type(post['draft_body'])}")
                if isinstance(post["draft_body"], dict):
                    logger.debug(
                        f"draft_body keys: {list(post['draft_body'].keys())[:10]}"
                    )

            # Extract the content in a readable format
            content = self._extract_readable_content(post)

            # Add debug info if content is empty
            # Remove debug info - tests expect clean output
            debug_info = ""

            result = {
                "id": post.get("id"),
                "title": post.get("title") or post.get("draft_title", "Untitled"),
                "subtitle": post.get("subtitle") or post.get("draft_subtitle", ""),
                "status": "published" if post.get("post_date") else "draft",
                "content": content,
                "publication_date": post.get("post_date"),
                "audience": post.get("audience", "everyone"),
            }

            return result

        except SubstackAPIError as e:
            # API errors should bubble up as-is
            logger.error(
                f"SubstackAPIError in get_post_content for post_id {post_id}: {str(e)}"
            )
            raise
        except AttributeError as e:
            # This is likely the 'str' object has no attribute 'get' error
            logger.error(
                f"AttributeError in get_post_content - API likely returned a string: {str(e)}"
            )
            logger.error(f"Exception type: {type(e)}, Full details: {repr(e)}")
            logger.error(
                f"Post variable type: {type(post) if 'post' in locals() else 'Not defined'}"
            )
            if "post" in locals() and isinstance(post, str):
                logger.error(f"Post is a string: {post}")
            raise ValueError(f"API returned invalid data format for post {post_id}")
        except Exception as e:
            logger.error(
                f"Unexpected error in get_post_content for post_id {post_id}: {str(e)}, type: {type(e)}"
            )
            raise ValueError(f"Failed to get content for post {post_id}: {str(e)}")

    async def duplicate_post(
        self, post_id: str, new_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a copy of an existing post as a new draft

        Args:
            post_id: The ID of the post to duplicate
            new_title: Optional title for the new draft (defaults to "Copy of [original]")

        Returns:
            The new draft post data
        """
        try:
            # Debug logging
            logger.debug(f"duplicate_post called with post_id: {post_id}")
            logger.debug(f"Client type: {type(self.client)}")
            logger.debug(f"Client class: {self.client.__class__.__name__}")
            logger.debug(
                f"Is APIWrapper: {self.client.__class__.__name__ == 'APIWrapper'}"
            )

            # Get the original post - wrapper should raise if string
            logger.debug(f"About to call client.get_draft({post_id})")
            original = self.client.get_draft(post_id)

            # Extra safety check
            if not isinstance(original, dict):
                logger.error(
                    f"Unexpected response type from Substack API: {type(original)}, value: {original}"
                )
                raise ValueError(
                    f"Invalid response from Substack API - expected dict, got {type(original)}"
                )

            # Extract title and content
            original_title = original.get("title") or original.get(
                "draft_title", "Untitled"
            )
            title = new_title or f"Copy of {original_title}"
            subtitle = original.get("subtitle") or original.get("draft_subtitle", "")

            # Extract content blocks
            # Safely get body - it could be a dict OR a JSON string
            body = original.get("body") or original.get("draft_body")

            if isinstance(body, str):
                # Try to parse JSON string
                try:
                    import json

                    parsed_body = json.loads(body)
                    if isinstance(parsed_body, dict) and "blocks" in parsed_body:
                        body = parsed_body
                    else:
                        # Not the expected format, create a text block
                        body = {
                            "blocks": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "content": body}],
                                }
                            ]
                        }
                except (json.JSONDecodeError, ValueError):
                    # Not JSON, create a text block
                    body = {
                        "blocks": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "content": body}],
                            }
                        ]
                    }
            elif not isinstance(body, dict):
                logger.warning(f"Original post body is not a dict: {type(body)}")
                body = {}

            blocks = body.get("blocks", [])

            # Create new post with same content
            user_id = self.client.get_user_id()
            post = Post(
                title=title,
                subtitle=subtitle,
                user_id=user_id,
                audience=original.get("audience", "everyone"),
            )

            # Add all blocks to the new post
            self._add_blocks_to_post(post, blocks)

            # Create the draft
            result = self.client.post_draft(post.get_draft())
            return result

        except SubstackAPIError as e:
            # API errors should bubble up as-is
            logger.error(
                f"SubstackAPIError in duplicate_post for post_id {post_id}: {str(e)}"
            )
            raise
        except AttributeError as e:
            # This is likely the 'str' object has no attribute 'get' error
            logger.error(
                f"AttributeError in duplicate_post - API likely returned a string: {str(e)}"
            )
            logger.error(f"Exception type: {type(e)}, Full details: {repr(e)}")
            logger.error(
                f"Original variable type: {type(original) if 'original' in locals() else 'Not defined'}"
            )
            if "original" in locals() and isinstance(original, str):
                logger.error(f"Original is a string: {original}")
            raise ValueError(f"API returned invalid data format for post {post_id}")
        except Exception as e:
            logger.error(
                f"Unexpected error in duplicate_post for post_id {post_id}: {str(e)}, type: {type(e)}"
            )
            raise ValueError(f"Failed to duplicate post {post_id}: {str(e)}")

    async def get_sections(self) -> List[Dict[str, Any]]:
        """Get available sections/categories for organizing posts

        Returns:
            List of sections with their IDs and names
        """
        sections = self.client.get_sections()
        return list(sections) if sections else []

    async def get_subscriber_count(self) -> Dict[str, Any]:
        """Get the total subscriber count for the publication

        Returns:
            Dictionary with subscriber count and other stats
        """
        try:
            # The API wrapper handles conversion and errors
            count = self.client.get_publication_subscriber_count()

            return {
                "total_subscribers": count,
                "publication_url": self.client.publication_url,
            }
        except Exception as e:
            logger.warning(
                f"Primary method failed: {str(e)}, trying alternative via sections"
            )

            # Try alternative method via sections
            try:
                # The API wrapper handles sections retrieval
                sections = self.client.get_sections()

                if sections and len(sections) > 0:
                    # Get subscriber count from first section
                    first_section = sections[0]
                    if isinstance(first_section, dict):
                        count = first_section.get("subscriber_count", 0)
                        return {
                            "total_subscribers": int(count),
                            "publication_url": self.client.publication_url,
                        }

                # If we get here, neither method worked
                raise ValueError(f"Unable to get subscriber count: {str(e)}")

            except Exception as e2:
                logger.error(
                    f"Both methods failed to get subscriber count: primary={str(e)}, sections={str(e2)}"
                )
                if isinstance(e, SubstackAPIError):
                    raise e
                raise SubstackAPIError(
                    f"Unable to get subscriber count (both methods failed)"
                )

    def _clean_publication_url(self, url: str) -> str:
        """Clean publication URL by removing API paths

        Args:
            url: The URL to clean

        Returns:
            Clean publication URL without API paths
        """
        if not url:
            return url

        # Remove /api/v1 or /api/v1/ if present
        clean_url = url.replace("/api/v1/", "/").replace("/api/v1", "")

        # Ensure it doesn't end with a slash
        if clean_url.endswith("/"):
            clean_url = clean_url[:-1]

        return clean_url

    async def preview_draft(self, post_id: str) -> Dict[str, Any]:
        """Get a preview link for a draft post

        Args:
            post_id: The ID of the draft to preview

        Returns:
            Preview information including shareable link
        """
        try:
            # First get the draft to check if it's published
            draft = self.client.get_draft(post_id)

            if not isinstance(draft, dict):
                logger.error(f"Unexpected draft response type: {type(draft)}")
                raise ValueError(f"Invalid draft response")

            # Extract slug from draft for published posts
            slug = draft.get("slug") or draft.get("draft_slug", "")

            # Try prepublish_draft to see if it returns a preview URL
            preview_url_from_api = None
            try:
                preview_data = self.client.prepublish_draft(post_id)
                logger.debug(f"prepublish_draft response: {preview_data}")

                if isinstance(preview_data, dict):
                    # Check for various possible URL fields
                    preview_url_from_api = (
                        preview_data.get("preview_url")
                        or preview_data.get("preview_link")
                        or preview_data.get("url")
                        or preview_data.get("draft_url")
                    )
                    if preview_url_from_api:
                        logger.info(
                            f"Found preview URL from API: {preview_url_from_api}"
                        )

                    # Also check for slug if we don't have one
                    if not slug:
                        slug = preview_data.get("slug") or preview_data.get(
                            "draft_slug", ""
                        )

            except Exception as e:
                logger.warning(
                    f"prepublish_draft failed (will construct URL manually): {str(e)}"
                )

            # Check if this is actually a draft (not published)
            # Check multiple fields that indicate published status
            is_published = (
                draft.get("post_date") is not None
                or draft.get("published_at") is not None
                or draft.get("is_published", False)
                or draft.get("published", False)
            )

            # If we got a preview URL from the API, use it
            if preview_url_from_api:
                preview_url = preview_url_from_api
                logger.info(f"Using preview URL from prepublish_draft API")
            elif self.client.publication_url:
                # Construct preview URL
                if is_published and slug:
                    # It's a published post, return the public URL
                    base_url = self._clean_publication_url(self.client.publication_url)
                    preview_url = f"{base_url}/p/{slug}"
                    logger.info(f"Post {post_id} is published, returning public URL")
                else:
                    # It's a draft, construct the author-only edit/preview URL
                    # Format: https://publication.substack.com/publish/post/{post_id}?back=%2Fpublish%2Fposts%2Fdrafts
                    import urllib.parse

                    base_url = self._clean_publication_url(self.client.publication_url)

                    # Build query parameters
                    params = {"back": "/publish/posts/drafts"}

                    query_string = urllib.parse.urlencode(params)
                    preview_url = f"{base_url}/publish/post/{post_id}?{query_string}"
                    logger.info(
                        f"Post {post_id} is a draft, returning author-only preview URL"
                    )

            # If we still don't have a URL, try edit URL format as fallback
            if not preview_url and self.client.publication_url:
                # Fallback: use the edit URL format
                base_url = self._clean_publication_url(self.client.publication_url)
                preview_url = f"{base_url}/publish/post/{post_id}"
                logger.info(f"Using fallback edit URL for post {post_id}")

            # Determine the type of URL for the message
            if preview_url:
                if "?postPreview=" in preview_url:
                    message = f"Draft preview link (share for feedback): {preview_url}"
                elif "/publish/post/" in preview_url:
                    message = f"Author-only preview link (not shareable - you must be logged in): {preview_url}"
                elif is_published:
                    message = f"Published post link: {preview_url}"
                else:
                    message = f"Preview link: {preview_url}"
            else:
                message = "Unable to generate preview URL"

            return {
                "post_id": post_id,
                "preview_url": preview_url,
                "title": draft.get("draft_title") or draft.get("title", "Untitled"),
                "is_published": is_published,
                "message": message,
            }

        except Exception as e:
            logger.error(
                f"Error in preview_draft for post_id {post_id}: {str(e)}, type: {type(e)}"
            )
            # Re-raise with more context
            if isinstance(e, SubstackAPIError):
                raise
            raise ValueError(f"Failed to generate preview for post {post_id}: {str(e)}")

    def _extract_readable_content(self, post: Dict[str, Any]) -> str:
        """Extract content from a post in a readable text format

        Args:
            post: The post data

        Returns:
            Readable text content
        """
        # Safely get body - it could be a dict OR a string
        body = post.get("body") or post.get("draft_body")
        logger.debug(f"_extract_readable_content - body type: {type(body)}")

        # If body is a string, it might be JSON
        if isinstance(body, str):
            logger.info(f"Body is a string. Length: {len(body)}")

            # Try to parse it as JSON
            try:
                import json

                parsed_body = json.loads(body)

                # Check for different JSON structures
                if isinstance(parsed_body, dict):
                    if "blocks" in parsed_body:
                        logger.info("Found blocks structure")
                        body = parsed_body
                        # Continue to process blocks below
                    elif parsed_body.get("type") == "doc" and "content" in parsed_body:
                        logger.info("Found doc/content structure, converting to blocks")
                        # This is a different format - convert content array to blocks
                        body = {"blocks": parsed_body["content"]}
                        # Continue to process blocks below
                    else:
                        # Unknown structure, return as-is
                        logger.warning(
                            f"Unknown JSON structure: {list(parsed_body.keys())[:5]}"
                        )
                        return body
                else:
                    # Not the expected format, return as-is
                    return body
            except (json.JSONDecodeError, ValueError):
                # Not JSON, return the string as-is
                logger.debug("Body string is not JSON, returning as plain text")
                return body

        # If body is not a dict, we can't extract blocks
        if not isinstance(body, dict):
            logger.warning(f"Post body is neither string nor dict: {type(body)}")
            return ""

        # Body is a dict, proceed with block extraction
        logger.debug(f"Body keys: {list(body.keys())[:10]}")

        blocks = body.get("blocks", [])
        logger.debug(f"Number of blocks: {len(blocks)}")
        if blocks:
            logger.debug(
                f"First block type: {blocks[0].get('type') if isinstance(blocks[0], dict) else 'not a dict'}"
            )

        content_parts = []
        for block in blocks:
            block_type = block.get("type")

            if block_type == "paragraph":
                text = self._extract_text_from_content(block.get("content", []))
                if text:
                    content_parts.append(text)

            elif (
                block_type in ["heading-one", "heading-two", "heading-three"]
                or block_type == "heading"
            ):
                text = self._extract_text_from_content(block.get("content", []))
                if text:
                    # Check if attrs contains level for new format
                    if block_type == "heading" and "attrs" in block:
                        level_num = block["attrs"].get("level", 1)
                        level = "#" * level_num
                    else:
                        level = {
                            "heading-one": "#",
                            "heading-two": "##",
                            "heading-three": "###",
                        }.get(block_type, "#")
                    content_parts.append(f"{level} {text}")

            elif block_type == "bulleted-list" or block_type == "bullet_list":
                items = block.get("content", [])
                for item in items:
                    if isinstance(item, dict):
                        item_text = ""

                        # Check if this is a list_item type
                        if item.get("type") == "list_item" and "content" in item:
                            # This is the structure from the real post
                            item_content = item["content"]
                            if isinstance(item_content, list) and item_content:
                                # Check if first element is a paragraph
                                first_elem = item_content[0]
                                if (
                                    isinstance(first_elem, dict)
                                    and first_elem.get("type") == "paragraph"
                                ):
                                    if "content" in first_elem:
                                        item_text = self._extract_text_from_content(
                                            first_elem["content"]
                                        )
                                else:
                                    item_text = self._extract_text_from_content(
                                        item_content
                                    )
                            else:
                                item_text = self._extract_text_from_content(
                                    item_content
                                )
                        # Check various possible fields
                        elif "text" in item and not "content" in item:
                            item_text = item["text"]
                        elif "paragraph" in item and not "content" in item:
                            # Some items have paragraph field instead of content
                            para = item["paragraph"]
                            if isinstance(para, dict) and "content" in para:
                                item_text = self._extract_text_from_content(
                                    para["content"]
                                )
                            else:
                                item_text = str(para)
                        elif "content" in item:
                            # List items can have nested structure - extract all content
                            item_content = item["content"]

                            if isinstance(item_content, str):
                                # Content is directly a string
                                item_text = item_content
                            elif isinstance(item_content, list):
                                # Try to extract text from all elements
                                text_parts = []
                                for elem in item_content:
                                    if isinstance(elem, dict):
                                        if (
                                            elem.get("type") == "paragraph"
                                            and "content" in elem
                                        ):
                                            extracted = self._extract_text_from_content(
                                                elem["content"]
                                            )
                                            if extracted:
                                                text_parts.append(extracted)
                                        elif (
                                            elem.get("type") == "text"
                                            and "text" in elem
                                        ):
                                            # Direct text node
                                            text_parts.append(elem["text"])
                                        else:
                                            # Try generic extraction
                                            extracted = self._extract_text_from_content(
                                                elem
                                            )
                                            if extracted:
                                                text_parts.append(extracted)

                                item_text = (
                                    " ".join(text_parts)
                                    if text_parts
                                    else "[empty bullet]"
                                )
                            else:
                                # Not a list, extract directly
                                item_text = (
                                    self._extract_text_from_content(item_content)
                                    or "[empty bullet]"
                                )

                        # Always add the bullet point, even if empty
                        content_parts.append(f"• {item_text}")

            elif block_type == "ordered-list":
                items = block.get("content", [])
                for i, item in enumerate(items, 1):
                    if isinstance(item, dict):
                        item_text = ""

                        # Check if this is a list_item type
                        if item.get("type") == "list_item" and "content" in item:
                            # This is the structure from the real post
                            item_content = item["content"]
                            if isinstance(item_content, list) and item_content:
                                # Check if first element is a paragraph
                                first_elem = item_content[0]
                                if (
                                    isinstance(first_elem, dict)
                                    and first_elem.get("type") == "paragraph"
                                ):
                                    if "content" in first_elem:
                                        item_text = self._extract_text_from_content(
                                            first_elem["content"]
                                        )
                                else:
                                    item_text = self._extract_text_from_content(
                                        item_content
                                    )
                            else:
                                item_text = self._extract_text_from_content(
                                    item_content
                                )
                        # Check various possible fields
                        elif "text" in item and not "content" in item:
                            item_text = item["text"]
                        elif "paragraph" in item and not "content" in item:
                            # Some items have paragraph field instead of content
                            para = item["paragraph"]
                            if isinstance(para, dict) and "content" in para:
                                item_text = self._extract_text_from_content(
                                    para["content"]
                                )
                            else:
                                item_text = str(para)
                        elif "content" in item:
                            # List items can have nested structure - extract all content
                            item_content = item["content"]

                            if isinstance(item_content, str):
                                # Content is directly a string
                                item_text = item_content
                            elif isinstance(item_content, list):
                                # Try to extract text from all elements
                                text_parts = []
                                for elem in item_content:
                                    if isinstance(elem, dict):
                                        if (
                                            elem.get("type") == "paragraph"
                                            and "content" in elem
                                        ):
                                            extracted = self._extract_text_from_content(
                                                elem["content"]
                                            )
                                            if extracted:
                                                text_parts.append(extracted)
                                        elif (
                                            elem.get("type") == "text"
                                            and "text" in elem
                                        ):
                                            # Direct text node
                                            text_parts.append(elem["text"])
                                        else:
                                            # Try generic extraction
                                            extracted = self._extract_text_from_content(
                                                elem
                                            )
                                            if extracted:
                                                text_parts.append(extracted)

                                item_text = (
                                    " ".join(text_parts)
                                    if text_parts
                                    else "[empty item]"
                                )
                            else:
                                # Not a list, extract directly
                                item_text = (
                                    self._extract_text_from_content(item_content)
                                    or "[empty item]"
                                )

                        # Always add the list item, even if empty
                        content_parts.append(f"{i}. {item_text}")

            elif block_type == "blockquote":
                text = self._extract_text_from_content(block.get("content", []))
                if text:
                    content_parts.append(f"> {text}")

            elif block_type == "code":
                code = block.get("content", "")
                if code:
                    content_parts.append(f"```\n{code}\n```")

            elif block_type == "hr":
                content_parts.append("---")

            elif block_type == "paywall":
                content_parts.append("<!-- PAYWALL -->")

            elif block_type in ["captioned-image", "captionedImage", "image", "image2"]:
                # Handle captioned-image, captionedImage, and plain image

                # Initialize defaults
                src = ""
                alt = "Image"
                caption_text = ""

                # Check multiple possible locations for image data
                if "attrs" in block:
                    # attrs on block level
                    attrs = block["attrs"]
                    # Check multiple possible URL field names in attrs
                    src = attrs.get("src") or attrs.get("url") or attrs.get("href", "")
                    alt = attrs.get("alt", "Image")
                elif "src" in block:
                    # Direct src/alt on block
                    src = block.get("src", "")
                    alt = block.get("alt", "Image")
                    caption_text = block.get("caption", "")
                elif "url" in block:
                    # Some images use 'url' instead of 'src'
                    src = block.get("url", "")
                    alt = block.get("alt", "Image")
                    caption_text = block.get("caption", "")
                elif "href" in block:
                    # Some images use 'href'
                    src = block.get("href", "")
                    alt = block.get("alt", "Image")
                    caption_text = block.get("caption", "")
                else:
                    # Check content block
                    content_block = block.get("content")

                    # Handle captionedImage with content array
                    if isinstance(content_block, list) and content_block:
                        # Look for image2 in content array
                        for elem in content_block:
                            if isinstance(elem, dict) and elem.get("type") == "image2":
                                attrs = elem.get("attrs", {})
                                src = attrs.get("src", "")
                                alt = attrs.get("alt", "Image")
                                break
                    elif isinstance(content_block, dict):
                        # New format: content is an object with type and attrs
                        attrs = content_block.get("attrs", {})
                        src = attrs.get("src", "")
                        alt = attrs.get("alt", "Image")
                        caption_blocks = block.get("content", [])
                        if isinstance(caption_blocks, list) and len(caption_blocks) > 1:
                            # Second item might be caption
                            caption_text = ""
                            for cap_block in caption_blocks[1:]:
                                if (
                                    isinstance(cap_block, dict)
                                    and cap_block.get("type") == "caption"
                                ):
                                    caption_text = self._extract_text_from_content(
                                        cap_block.get("content", [])
                                    )
                        else:
                            caption_text = ""
                    else:
                        # Old format
                        alt = block.get("alt", "Image")
                        src = block.get("src", "")
                        caption_text = block.get("caption", "")

                # Always add image, even without src
                content_parts.append(f"![{alt}]({src})")
                if caption_text:
                    content_parts.append(f"*{caption_text}*")

            # Add spacing between blocks
            if content_parts and block_type != "paywall":
                content_parts.append("")

        return "\n".join(content_parts).strip()

    def _convert_content_to_blocks(
        self, content: str, content_type: str
    ) -> List[Dict[str, Any]]:
        """Convert content to Substack blocks based on content type

        Args:
            content: The content to convert
            content_type: Type of content ("markdown", "html", or "plain")

        Returns:
            List of Substack blocks

        Raises:
            ValueError: If content_type is not supported
        """
        if content_type == "markdown":
            return self.markdown_converter.convert(content)
        elif content_type == "html":
            return self.html_converter.convert(content)
        elif content_type == "plain":
            return self._plain_text_to_blocks(content)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    def _plain_text_to_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Convert plain text to paragraph blocks

        Args:
            content: Plain text content

        Returns:
            List of paragraph blocks
        """
        blocks = []
        paragraphs = content.split("\n\n")

        for paragraph in paragraphs:
            if paragraph.strip():
                blocks.append(self.block_builder.paragraph(paragraph.strip()))

        return blocks

    def _process_paywall_markers(
        self, content: str, blocks: List[Dict[str, Any]], content_type: str
    ) -> List[Dict[str, Any]]:
        """Process paywall markers in content

        Args:
            content: Original content string
            blocks: Converted blocks
            content_type: Type of content

        Returns:
            Blocks with paywall markers inserted
        """
        # Check for paywall markers (support multiple formats)
        paywall_markers = [
            "<!-- PAYWALL -->",
            "<!--PAYWALL-->",
            "<!--paywall-->",
            "<!-- paywall -->",
        ]
        paywall_marker = None

        for marker in paywall_markers:
            if content_type == "markdown" and marker in content:
                paywall_marker = marker
                break

        if paywall_marker:
            # Find where to insert paywall block
            new_blocks = []

            # Split content by paywall marker to determine position
            parts = content.split(paywall_marker)
            if len(parts) > 1:
                # Convert first part to blocks
                first_part_blocks = self.markdown_converter.convert(parts[0])
                new_blocks.extend(first_part_blocks)

                # Add paywall block
                new_blocks.append(self.block_builder.paywall())

                # Convert remaining parts
                for part in parts[1:]:
                    if part.strip():
                        part_blocks = self.markdown_converter.convert(part)
                        new_blocks.extend(part_blocks)

                return new_blocks

        return blocks

    def _format_blocks_for_api(self, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format blocks for Substack API

        Args:
            blocks: List of block dictionaries

        Returns:
            Formatted body object for API
        """
        return {"blocks": blocks}

    def _add_blocks_to_post(self, post: Post, blocks: List[Dict[str, Any]]):
        """Add blocks to a Post object using the correct python-substack methods

        Args:
            post: The Post object to add content to
            blocks: List of block dictionaries to add
        """
        for block in blocks:
            block_type = block.get("type")
            content = block.get("content")

            if block_type == "paragraph":
                # Extract text and add as single paragraph
                text_content = self._extract_text_from_content(content)
                post.paragraph(text_content)

            elif block_type in [
                "heading-one",
                "heading-two",
                "heading-three",
                "heading-four",
                "heading-five",
                "heading-six",
            ]:
                level_map = {
                    "one": 1,
                    "two": 2,
                    "three": 3,
                    "four": 4,
                    "five": 5,
                    "six": 6,
                }
                level_text = block_type.split("-")[1]
                actual_level = level_map.get(level_text, 1)
                # Extract text from AST structure
                text_content = self._extract_text_from_content(content)
                post.heading(text_content, actual_level)

            elif block_type == "hr":
                post.horizontal_rule()

            elif block_type == "paywall":
                # Add paywall block - the library doesn't have a direct method, so use add()
                post.add({"type": "paywall"})

            elif block_type == "captioned-image":
                # Convert to paragraph with markdown - this is the only reliable way
                image_src = block.get("src", "")
                image_alt = block.get("alt", "")
                image_caption = block.get("caption", "")

                # Create markdown image syntax
                image_markdown = f"![{image_alt}]({image_src})"
                if image_caption:
                    image_markdown += f"\n\n*{image_caption}*"

                # Add as a regular paragraph
                post.paragraph(image_markdown)

            elif block_type == "code":
                # Code blocks - add as proper code_block type
                code_content = block.get("content", "")
                language = block.get("language", "")

                # Enhance readability by adding language comment at the top
                enhanced_content = code_content
                if language:
                    # Add language identifier as a comment for clarity
                    language_upper = language.upper()
                    comment_char = self._get_comment_char(language)
                    if comment_char:
                        separator = "=" * 20
                        header = f"{comment_char} {separator} {language_upper} CODE {separator}"
                        # Only add header if it's not already present
                        if not code_content.startswith(header):
                            enhanced_content = f"{header}\n{code_content}"

                # The python-substack library expects the content as a raw string
                code_block = {"type": "code_block", "content": enhanced_content}

                # Include language attrs for future compatibility
                if language:
                    code_block["attrs"] = {"language": language}

                post.add(code_block)

            elif block_type in ["bulleted-list", "ordered-list"]:
                # Lists - convert to formatted paragraphs
                list_items = block.get("content", [])
                for i, item in enumerate(list_items, 1):
                    if isinstance(item, dict) and "content" in item:
                        item_content = item["content"]
                        if isinstance(item_content, list) and len(item_content) > 0:
                            # Extract text from the paragraph content
                            para_content = self._extract_text_from_content(
                                item_content[0].get("content", [])
                            )
                            prefix = "• " if block_type == "bulleted-list" else f"{i}. "
                            post.paragraph(f"{prefix}{para_content}")

            elif block_type == "blockquote":
                # Extract text from blockquote content
                quote_text = self._extract_text_from_content(content)
                post.paragraph(f"> {quote_text}")

            else:
                # Fallback: extract text and add as paragraph
                if content:
                    text_content = self._extract_text_from_content(content)
                    if text_content:
                        post.paragraph(text_content)

    def _extract_text_from_content(self, content) -> str:
        """Extract plain text from AST content structure

        Args:
            content: Content from block (can be string, list, or dict)

        Returns:
            Plain text string with formatting applied
        """
        if isinstance(content, str):
            return content

        elif isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    item_type = item.get("type")
                    item_content = item.get("content", "")

                    # Handle nested structures recursively
                    if item_type in ["paragraph", "text"]:
                        if item_type == "text":
                            # This is a text node with possible formatting
                            # Check both 'content' and 'text' fields
                            text = item.get("text") or item.get("content", "")
                            text = str(text) if text else ""
                            marks = item.get("marks", [])

                            # Apply formatting based on marks
                            for mark in marks:
                                mark_type = mark.get("type")
                                if mark_type == "strong":
                                    text = f"**{text}**"
                                elif mark_type == "em":
                                    text = f"*{text}*"
                                elif mark_type == "code":
                                    text = f"`{text}`"
                                elif mark_type == "link":
                                    # Check both direct href and attrs.href
                                    href = mark.get("href")
                                    if not href and "attrs" in mark:
                                        href = mark["attrs"].get("href", "#")
                                    if not href:
                                        href = "#"
                                    text = f"[{text}]({href})"

                            text_parts.append(text)
                        else:
                            # This is a paragraph, recursively extract its content
                            text_parts.append(
                                self._extract_text_from_content(item_content)
                            )
                    else:
                        # For other types, try to extract content recursively
                        text_parts.append(self._extract_text_from_content(item_content))

                elif isinstance(item, str):
                    text_parts.append(item)

            return "".join(text_parts)

        elif isinstance(content, dict):
            # Handle dict content recursively
            return self._extract_text_from_content(content.get("content", ""))

        return str(content)

    def _add_formatted_content_to_paragraph(self, para, content):
        """Add formatted content to a paragraph object

        Args:
            para: The paragraph object from Post
            content: The content list from the AST
        """
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get(
                        "content", item.get("text", "")
                    )  # Check both 'content' and 'text'
                    marks = item.get("marks", [])

                    # Add text first
                    para.text(text)

                    # Then apply marks if any
                    if (
                        marks and len(marks) > 0
                    ):  # Only call marks() if we have actual marks
                        para.marks(marks)

        elif isinstance(content, str):
            para.text(content)

    def _convert_content_to_text_nodes(self, content):
        """Convert AST content to proper text nodes with marks

        Args:
            content: Content from AST

        Returns:
            List of text nodes with proper marks
        """
        if isinstance(content, list):
            nodes = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    node = {"type": "text", "text": item.get("content", "")}
                    if "marks" in item and item["marks"]:
                        node["marks"] = item["marks"]
                    nodes.append(node)
            return nodes
        return []

    def _get_comment_char(self, language: str) -> str:
        """Get the appropriate comment character for a language

        Args:
            language: Programming language name

        Returns:
            Comment character(s) for that language
        """
        comment_chars = {
            "python": "#",
            "python3": "#",
            "py": "#",
            "ruby": "#",
            "rb": "#",
            "perl": "#",
            "bash": "#",
            "sh": "#",
            "shell": "#",
            "yaml": "#",
            "yml": "#",
            "makefile": "#",
            "r": "#",
            "julia": "#",
            "elixir": "#",
            "javascript": "//",
            "js": "//",
            "typescript": "//",
            "ts": "//",
            "java": "//",
            "c": "//",
            "cpp": "//",
            "c++": "//",
            "csharp": "//",
            "cs": "//",
            "go": "//",
            "golang": "//",
            "rust": "//",
            "rs": "//",
            "swift": "//",
            "kotlin": "//",
            "php": "//",
            "dart": "//",
            "scala": "//",
            "groovy": "//",
            "sql": "--",
            "postgresql": "--",
            "mysql": "--",
            "lua": "--",
            "haskell": "--",
            "elm": "--",
            "html": "<!--",
            "xml": "<!--",
            "css": "/*",
            "scss": "/*",
            "sass": "//",
            "less": "//",
            "lisp": ";",
            "clojure": ";",
            "scheme": ";",
            "asm": ";",
            "assembly": ";",
            "vb": "'",
            "vbnet": "'",
            "basic": "'",
            "matlab": "%",
            "octave": "%",
            "latex": "%",
            "tex": "%",
            "fortran": "!",
            "f90": "!",
            "ada": "--",
            "pascal": "//",
            "delphi": "//",
        }

        # Return the comment character for the language, default to #
        return comment_chars.get(language.lower(), "#")
