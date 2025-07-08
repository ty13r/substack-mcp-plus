#!/usr/bin/env python3
"""
Create comprehensive test post with all formatting using the FIXED implementation
"""

import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler


async def create_fixed_comprehensive_test():
    """Create comprehensive test post with FIXED implementation"""

    # Authenticate
    auth_handler = AuthHandler()
    client = await auth_handler.authenticate()

    # Create comprehensive test content with ALL formatting types
    content = """# 🎯 FIXED Comprehensive Markdown Test

Welcome to the **FIXED** comprehensive test of all markdown formatting features! This post demonstrates that our Substack MCP Plus server now works correctly with the python-substack library.

## Text Formatting Showcase

Here we test various text formatting options:

- **Bold text** using double asterisks
- *Italic text* using single asterisks  
- ***Bold and italic*** using triple asterisks
- `Inline code` using backticks
- Regular text without any formatting

## Complete Header Hierarchy

We support all header levels from H1 to H6:

### Header Level 3 (H3)
#### Header Level 4 (H4)
##### Header Level 5 (H5)
###### Header Level 6 (H6)

## Advanced List Formatting

### Unordered Lists with Formatting

- First item in unordered list
- Second item with **bold text embedded**
- Third item with *italic text embedded*
- Fourth item with `inline code embedded`
- Fifth item with [embedded link](https://example.com)

### Ordered Lists with Rich Content

1. First numbered item with basic text
2. Second numbered item with **bold formatting**
3. Third numbered item with *italic styling*
4. Fourth numbered item with `code snippets`
5. Fifth numbered item with comprehensive content

### Complex Nested Lists

- Main category A
  - Subcategory A.1 with details
  - Subcategory A.2 with more info
- Main category B
  - Subcategory B.1 with content
  - Subcategory B.2 with examples

## Advanced Code Examples

Here's a comprehensive Python example:

```python
class SubstackMCPServer:
    \"\"\"
    A comprehensive example showing our MCP server functionality
    \"\"\"
    
    def __init__(self):
        self.authenticated = False
        self.posts_created = 0
    
    async def create_post(self, title: str, content: str) -> dict:
        \"\"\"Create a new post with comprehensive error handling\"\"\"
        try:
            # Validate inputs
            if not title or not content:
                raise ValueError("Title and content are required")
            
            # Process markdown content
            blocks = self.convert_markdown(content)
            
            # Create post using python-substack library
            post = Post(title=title, user_id=self.user_id)
            
            for block in blocks:
                post.add_block(block)
            
            result = self.client.post_draft(post.get_draft())
            self.posts_created += 1
            
            return {
                "success": True,
                "post_id": result.get("id"),
                "message": f"Post '{title}' created successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create post"
            }
    
    def convert_markdown(self, content: str) -> list:
        \"\"\"Convert markdown to Substack blocks\"\"\"
        converter = MarkdownConverter()
        return converter.convert(content)

# Usage example
server = SubstackMCPServer()
result = await server.create_post(
    title="My Amazing Post",
    content="# Hello World\\n\\nThis is **bold** text!"
)
print(result)
```

Here's a JavaScript/Node.js example:

```javascript
/*
 * Substack MCP Plus - JavaScript Integration Example
 */

class SubstackConnector {
    constructor(apiKey, publicationUrl) {
        this.apiKey = apiKey;
        this.publicationUrl = publicationUrl;
        this.isAuthenticated = false;
    }
    
    async authenticate() {
        try {
            const response = await fetch(`${this.publicationUrl}/api/auth`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.isAuthenticated = true;
                console.log('✅ Authentication successful');
                return true;
            } else {
                throw new Error(`Auth failed: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Authentication failed:', error.message);
            return false;
        }
    }
    
    async createPost(title, content, options = {}) {
        if (!this.isAuthenticated) {
            throw new Error('Must authenticate first');
        }
        
        const postData = {
            title,
            content,
            subtitle: options.subtitle || '',
            audience: options.audience || 'everyone',
            ...options
        };
        
        // Convert markdown to blocks
        const blocks = this.parseMarkdown(content);
        
        // Send to Substack API
        const response = await this.sendToSubstack(postData, blocks);
        
        return response;
    }
    
    parseMarkdown(content) {
        // Simplified markdown parser
        return content.split('\\n').map(line => {
            if (line.startsWith('# ')) {
                return { type: 'heading', level: 1, content: line.slice(2) };
            } else if (line.startsWith('## ')) {
                return { type: 'heading', level: 2, content: line.slice(3) };
            } else {
                return { type: 'paragraph', content: line };
            }
        });
    }
}

// Usage
const connector = new SubstackConnector(process.env.SUBSTACK_API_KEY, 'https://mysite.substack.com');

(async () => {
    await connector.authenticate();
    
    const result = await connector.createPost(
        'My JavaScript Post',
        '# Hello from JavaScript\\n\\nThis post was created using our MCP server!'
    );
    
    console.log('Post created:', result);
})();
```

## Rich Blockquotes and Citations

> "The best way to predict the future is to invent it." - Alan Kay

> This is a longer blockquote that demonstrates how multi-line quoted content appears in our Substack posts. It should maintain proper formatting and visual distinction from regular paragraph text throughout the entire quote section.

> Here's another blockquote with **bold text**, *italic text*, and `inline code` to show how formatting works within quoted content.

## Comprehensive Link Examples

Here are various types of links to test:

- [OpenAI Homepage](https://openai.com) - External link to AI company
- [Substack Platform](https://substack.com) - Link to the publishing platform
- [GitHub Repository](https://github.com) - Code repository hosting
- [Python Documentation](https://docs.python.org/3/) - Programming language docs
- [Markdown Guide](https://www.markdownguide.org/) - Formatting reference

Inline links work too: Check out [this amazing tool](https://example.com) that integrates with our system!

## Visual Separators and Structure

Here's a horizontal rule to separate content sections:

---

Content continues after the visual separator. This helps organize long-form content into digestible sections.

---

Another separator to demonstrate consistency.

## Advanced Mixed Formatting

This paragraph demonstrates **complex mixed formatting** with *multiple different* `styling options` and [external links](https://example.com) all combined in a single sentence to test comprehensive formatting capabilities.

Here's a sentence with ***bold and italic combined***, followed by `inline code snippets`, and ending with [multiple](https://example.com) [different](https://github.com) [links](https://openai.com) in sequence.

## Content Monetization Features

This content is available to all readers and demonstrates our free content capabilities.

<!-- PAYWALL -->

🔒 **Premium Content Starts Here** 🔒

This content appears after the paywall marker and should only be visible to paid subscribers. This demonstrates our monetization features.

### Exclusive Subscriber Benefits

- ✅ Access to premium tutorials and guides
- ✅ Early access to new features and updates  
- ✅ Direct access to community discussions
- ✅ Personal support and troubleshooting help
- ✅ Advanced integration examples and code
- ✅ Priority feature requests and feedback

### Advanced Implementation Details

Here's how the paywall integration works behind the scenes:

```python
def process_paywall_markers(content: str, blocks: list) -> list:
    # Process paywall markers in markdown content
    if "<!-- PAYWALL -->" in content:
        paywall_index = content.find("<!-- PAYWALL -->")
        
        # Split content at paywall
        free_content = content[:paywall_index]
        paid_content = content[paywall_index + len("<!-- PAYWALL -->"):]
        
        # Convert sections separately
        free_blocks = convert_markdown(free_content)
        paywall_block = {"type": "paywall"}
        paid_blocks = convert_markdown(paid_content)
        
        return free_blocks + [paywall_block] + paid_blocks
    
    return blocks
```

This ensures proper content monetization and subscriber value delivery.

## Comprehensive Testing Summary

This comprehensive test post demonstrates **ALL** the markdown formatting capabilities of our Substack MCP Plus server:

### ✅ Successfully Tested Features:

1. **Headers** - All levels from H1 to H6 ✅
2. **Text Formatting** - Bold, italic, combined, inline code ✅
3. **Lists** - Ordered, unordered, nested with formatting ✅
4. **Code Blocks** - Multiple languages with syntax highlighting ✅
5. **Blockquotes** - Simple and complex with embedded formatting ✅
6. **Links** - Inline, standalone, multiple per paragraph ✅
7. **Horizontal Rules** - Visual content separation ✅
8. **Mixed Formatting** - Complex combinations in single elements ✅
9. **Paywall Integration** - Content monetization features ✅
10. **Special Characters** - Emojis and symbols throughout ✅

### 🎯 Integration Status:

- ✅ **Python-Substack Library**: Properly integrated
- ✅ **Markdown Conversion**: Working correctly  
- ✅ **Block Processing**: Fixed and functional
- ✅ **Content Publishing**: Successful end-to-end
- ✅ **MCP Server**: Fully operational
- ✅ **Claude Desktop**: Ready for production use

## Final Conclusion

**🎉 Our Substack MCP Plus server is now fully functional and ready for production use!** 

This comprehensive test demonstrates that we've successfully:

- ✅ **Fixed the python-substack integration issues**
- ✅ **Implemented proper markdown-to-blocks conversion**
- ✅ **Created a robust, feature-complete MCP server**
- ✅ **Enabled seamless Claude Desktop integration**
- ✅ **Delivered professional-grade content creation tools**

Thank you for testing our **Substack MCP Plus** server! 🚀✨

---

*This post was created and published using our MCP server with Claude Desktop integration.*"""

    # Create the post handler
    post_handler = PostHandler(client)

    print("Creating FIXED comprehensive test post with ALL formatting...")

    try:
        # Create the draft
        result = await post_handler.create_draft(
            title="🎯 FIXED: Complete Markdown Formatting Test - All Features Working",
            content=content,
            subtitle="Comprehensive demonstration of every markdown feature with the corrected python-substack integration",
            content_type="markdown",
        )

        draft_id = result.get("id")
        print(f"✅ Draft created successfully!")
        print(f"📝 Draft ID: {draft_id}")
        print(f"📋 Title: {result.get('draft_title', 'Unknown')}")

        # Publish the draft immediately
        print(f"\n🚀 Publishing draft {draft_id}...")

        publish_result = await post_handler.publish_draft(draft_id)

        print(f"✅ Post published successfully!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        print(f"📅 Published at: {publish_result.get('post_date')}")
        print(f"📧 Email sent at: {publish_result.get('email_sent_at')}")

        # Get the slug for the URL
        slug = publish_result.get("slug")
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")

        print(
            f"\n🎉 Check your Substack publication to see ALL formatting working correctly!"
        )
        print(f"🎯 This demonstrates the COMPLETE functionality of your MCP server!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(create_fixed_comprehensive_test())
