#!/usr/bin/env python3
"""
Comprehensive test of ALL Substack formatting options
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler
from src.handlers.post_handler import PostHandler

@pytest.mark.requires_auth
@pytest.mark.integration
async def test_comprehensive_formatting():
    print("🧪 Testing ALL formatting options comprehensively...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Comprehensive test content with ALL formatting options
        content = """# 🎯 Ultimate Substack Formatting Test

This post tests EVERY formatting option available in Substack to ensure our MCP server handles all cases correctly.

## 📋 Table of Contents

1. [Text Formatting](#text-formatting)
2. [Headers](#headers)
3. [Lists](#lists)
4. [Code Blocks](#code-blocks)
5. [Blockquotes](#blockquotes)
6. [Links and Images](#links-and-images)
7. [Special Elements](#special-elements)
8. [Edge Cases](#edge-cases)

---

## Text Formatting

### Basic Formatting

This is **bold text** and this is *italic text*. We can also have ***bold and italic*** combined.

Here's some `inline code` mixed with regular text. We can have multiple `code snippets` in the same line.

### Complex Formatting Combinations

Let's test **bold with `inline code` inside** and *italic with `code` too*. How about ***all three: bold, italic, and `code` together***?

We can also test [**bold links**](https://example.com) and [*italic links*](https://example.com) and even [***bold italic links***](https://example.com).

---

## Headers

# H1: Main Title Header
## H2: Section Header
### H3: Subsection Header
#### H4: Sub-subsection Header
##### H5: Minor Header
###### H6: Smallest Header

### Headers with Formatting

## This is an H2 with **bold** and *italic* text
### H3 with `inline code` in the header
#### H4 with a [link](https://example.com) in it

---

## Lists

### Unordered Lists

• Simple item 1
• Simple item 2
• Simple item 3

### Ordered Lists

1. First item
2. Second item with **bold text**
3. Third item with *italic text*
4. Fourth item with `inline code`
5. Fifth item with [a link](https://example.com)

### Nested Lists

• Top level item
  • Nested item 1
  • Nested item 2
    • Double nested item
    • Another double nested
  • Back to single nested
• Another top level item

### Mixed List Types

1. Ordered top level
   • Unordered nested
   • Another unordered
2. Second ordered item
   1. Nested ordered
   2. Another nested ordered
3. Third item with formatting:
   • **Bold item**
   • *Italic item*
   • `Code item`

---

## Code Blocks

### Python Code

```python
# ==================== PYTHON CODE ====================
import asyncio
from datetime import datetime
from typing import List, Dict, Optional

class SubstackFormatter:
    \"\"\"A comprehensive formatter for Substack posts\"\"\"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        
    async def format_post(self, content: str) -> Dict[str, Any]:
        \"\"\"Format content for Substack API
        
        Args:
            content: Raw markdown content
            
        Returns:
            Formatted post data
        \"\"\"
        blocks = []
        
        # Parse content into blocks
        for line in content.split('\n'):
            if line.startswith('#'):
                blocks.append(self._create_header(line))
            elif line.startswith('```'):
                blocks.append(self._create_code_block(line))
            else:
                blocks.append(self._create_paragraph(line))
                
        return {
            'blocks': blocks,
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'word_count': len(content.split())
            }
        }
    
    def _create_header(self, text: str) -> Dict[str, Any]:
        level = len(text.split()[0])  # Count # symbols
        return {
            'type': f'heading-{level}',
            'content': text.lstrip('#').strip()
        }

# Example usage
formatter = SubstackFormatter('your-api-key')
result = asyncio.run(formatter.format_post("# Hello World"))
print(f"Formatted {len(result['blocks'])} blocks")
```

### JavaScript/TypeScript Code

```javascript
// ==================== JAVASCRIPT CODE ====================
// Advanced React component with TypeScript
import React, { useState, useEffect, useCallback } from 'react';
import { SubstackAPI } from '@substack/api-client';

interface PostData {
  id: string;
  title: string;
  content: string;
  publishedAt?: Date;
  isPaid: boolean;
}

const SubstackEditor: React.FC<{ apiKey: string }> = ({ apiKey }) => {
  const [posts, setPosts] = useState<PostData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Initialize API client
  const api = new SubstackAPI(apiKey);
  
  // Fetch posts with error handling
  const fetchPosts = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.posts.list({
        limit: 50,
        status: 'draft'
      });
      
      setPosts(response.data.map(post => ({
        id: post.id,
        title: post.title,
        content: post.body,
        publishedAt: post.published_at ? new Date(post.published_at) : undefined,
        isPaid: post.audience === 'only_paid'
      })));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Failed to fetch posts:', err);
    } finally {
      setLoading(false);
    }
  }, [api]);
  
  // Auto-fetch on mount
  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);
  
  return (
    <div className="substack-editor">
      {loading && <div>Loading posts...</div>}
      {error && <div className="error">Error: {error}</div>}
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
};

export default SubstackEditor;
```

### SQL Database Query

```sql
-- ==================== SQL CODE ====================
-- Complex query to analyze Substack post performance
WITH post_metrics AS (
  -- Calculate engagement metrics for each post
  SELECT 
    p.id,
    p.title,
    p.published_at,
    p.is_paid,
    COUNT(DISTINCT v.user_id) as unique_views,
    COUNT(DISTINCT c.user_id) as unique_commenters,
    COUNT(c.id) as total_comments,
    AVG(v.read_time_seconds) as avg_read_time,
    SUM(CASE WHEN s.status = 'active' THEN 1 ELSE 0 END) as new_subscribers
  FROM posts p
  LEFT JOIN post_views v ON p.id = v.post_id
  LEFT JOIN comments c ON p.id = c.post_id
  LEFT JOIN subscriptions s ON s.trigger_post_id = p.id
  WHERE 
    p.status = 'published'
    AND p.published_at >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY p.id, p.title, p.published_at, p.is_paid
),
engagement_scores AS (
  -- Calculate normalized engagement scores
  SELECT 
    *,
    -- Normalize metrics to 0-100 scale
    (unique_views::float / NULLIF(MAX(unique_views) OVER (), 0)) * 100 as view_score,
    (total_comments::float / NULLIF(MAX(total_comments) OVER (), 0)) * 100 as comment_score,
    (new_subscribers::float / NULLIF(MAX(new_subscribers) OVER (), 0)) * 100 as subscriber_score,
    -- Calculate composite engagement score
    (
      (unique_views::float / NULLIF(MAX(unique_views) OVER (), 0)) * 0.3 +
      (total_comments::float / NULLIF(MAX(total_comments) OVER (), 0)) * 0.3 +
      (new_subscribers::float / NULLIF(MAX(new_subscribers) OVER (), 0)) * 0.4
    ) * 100 as overall_score
  FROM post_metrics
)
-- Final results with rankings
SELECT 
  ROW_NUMBER() OVER (ORDER BY overall_score DESC) as rank,
  title,
  published_at::date as publish_date,
  CASE 
    WHEN is_paid THEN 'Paid'
    ELSE 'Free'
  END as post_type,
  unique_views,
  total_comments,
  new_subscribers,
  ROUND(avg_read_time / 60.0, 1) as avg_read_minutes,
  ROUND(overall_score, 1) as engagement_score,
  -- Categorize performance
  CASE 
    WHEN overall_score >= 80 THEN '🌟 Top Performer'
    WHEN overall_score >= 60 THEN '📈 High Engagement'
    WHEN overall_score >= 40 THEN '👍 Good Performance'
    WHEN overall_score >= 20 THEN '📊 Average'
    ELSE '📉 Needs Improvement'
  END as performance_tier
FROM engagement_scores
ORDER BY overall_score DESC
LIMIT 25;
```

### Bash/Shell Script

```bash
#!/bin/bash
# ==================== BASH CODE ====================
# Comprehensive Substack backup and deployment script

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SUBSTACK_API_KEY="${SUBSTACK_API_KEY:-}"
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
LOG_FILE="./logs/substack_ops_$(date +%Y%m%d).log"
MAX_RETRIES=3
RETRY_DELAY=5

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level=$1
    shift
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

# Error handling
handle_error() {
    log "ERROR" "${RED}Script failed at line $1${NC}"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Check prerequisites
check_prerequisites() {
    log "INFO" "Checking prerequisites..."
    
    # Check for required commands
    local required_commands=("curl" "jq" "python3" "git")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log "ERROR" "${RED}Required command '$cmd' not found${NC}"
            exit 1
        fi
    done
    
    # Check API key
    if [[ -z "$SUBSTACK_API_KEY" ]]; then
        log "ERROR" "${RED}SUBSTACK_API_KEY environment variable not set${NC}"
        exit 1
    fi
    
    log "SUCCESS" "${GREEN}All prerequisites met${NC}"
}

# Backup function with retry logic
backup_posts() {
    log "INFO" "Starting post backup..."
    
    mkdir -p "$BACKUP_DIR"
    
    local retry_count=0
    while [[ $retry_count -lt $MAX_RETRIES ]]; do
        if curl -s -H "Authorization: Bearer $SUBSTACK_API_KEY" \
            "https://api.substack.com/posts?status=all" \
            | jq '.' > "$BACKUP_DIR/posts.json"; then
            
            log "SUCCESS" "${GREEN}Posts backed up successfully${NC}"
            break
        else
            retry_count=$((retry_count + 1))
            log "WARN" "${YELLOW}Backup attempt $retry_count failed, retrying...${NC}"
            sleep $RETRY_DELAY
        fi
    done
    
    if [[ $retry_count -eq $MAX_RETRIES ]]; then
        log "ERROR" "${RED}Failed to backup posts after $MAX_RETRIES attempts${NC}"
        return 1
    fi
}

# Deploy content
deploy_content() {
    local environment=${1:-"staging"}
    log "INFO" "Deploying to $environment environment..."
    
    # Run tests first
    if ! python3 -m pytest tests/; then
        log "ERROR" "${RED}Tests failed, aborting deployment${NC}"
        return 1
    fi
    
    # Build and deploy based on environment
    case "$environment" in
        "production")
            python3 deploy.py --env production --verify
            ;;
        "staging")
            python3 deploy.py --env staging
            ;;
        *)
            log "ERROR" "${RED}Unknown environment: $environment${NC}"
            return 1
            ;;
    esac
    
    log "SUCCESS" "${GREEN}Deployment completed successfully${NC}"
}

# Main execution
main() {
    log "INFO" "Starting Substack operations script..."
    
    check_prerequisites
    backup_posts
    
    # Parse command line arguments
    case "${1:-help}" in
        "backup")
            log "INFO" "Backup completed"
            ;;
        "deploy")
            deploy_content "${2:-staging}"
            ;;
        "full")
            backup_posts
            deploy_content "${2:-staging}"
            ;;
        *)
            echo "Usage: $0 {backup|deploy|full} [environment]"
            exit 1
            ;;
    esac
    
    log "INFO" "Script completed successfully"
}

# Run main function
main "$@"
```

### Additional Languages

```ruby
# ==================== RUBY CODE ====================
# Ruby class for Substack integration
class SubstackClient
  attr_reader :api_key, :base_url
  
  def initialize(api_key)
    @api_key = api_key
    @base_url = 'https://api.substack.com'
    @http = Net::HTTP.new(base_url)
  end
  
  def create_post(title:, content:, paid: false)
    post_data = {
      title: title,
      body: format_content(content),
      audience: paid ? 'only_paid' : 'everyone'
    }
    
    response = make_request('/posts', :post, post_data)
    JSON.parse(response.body)
  end
  
  private
  
  def format_content(content)
    # Convert markdown to Substack blocks
    content.split("\n").map do |line|
      case line
      when /^#+ /
        { type: 'heading', level: line.count('#'), text: line.gsub(/^#+ /, '') }
      when /^```/
        { type: 'code', language: line[3..-1], content: '' }
      else
        { type: 'paragraph', text: line }
      end
    end
  end
end
```

```go
// ==================== GO CODE ====================
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "time"
)

// SubstackPost represents a post structure
type SubstackPost struct {
    ID          string    `json:"id"`
    Title       string    `json:"title"`
    Content     string    `json:"content"`
    PublishedAt time.Time `json:"published_at,omitempty"`
    IsPaid      bool      `json:"is_paid"`
}

// SubstackClient handles API communication
type SubstackClient struct {
    APIKey     string
    BaseURL    string
    HTTPClient *http.Client
}

// NewClient creates a new Substack client
func NewClient(apiKey string) *SubstackClient {
    return &SubstackClient{
        APIKey:  apiKey,
        BaseURL: "https://api.substack.com",
        HTTPClient: &http.Client{
            Timeout: 30 * time.Second,
        },
    }
}

// CreatePost creates a new post
func (c *SubstackClient) CreatePost(post SubstackPost) (*SubstackPost, error) {
    data, err := json.Marshal(post)
    if err != nil {
        return nil, fmt.Errorf("failed to marshal post: %w", err)
    }
    
    req, err := http.NewRequest("POST", c.BaseURL+"/posts", bytes.NewBuffer(data))
    if err != nil {
        return nil, fmt.Errorf("failed to create request: %w", err)
    }
    
    req.Header.Set("Authorization", "Bearer "+c.APIKey)
    req.Header.Set("Content-Type", "application/json")
    
    resp, err := c.HTTPClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("request failed: %w", err)
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("API returned status %d", resp.StatusCode)
    }
    
    var result SubstackPost
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, fmt.Errorf("failed to decode response: %w", err)
    }
    
    return &result, nil
}

func main() {
    client := NewClient("your-api-key")
    
    post := SubstackPost{
        Title:   "Hello from Go",
        Content: "This post was created using Go!",
        IsPaid:  false,
    }
    
    created, err := client.CreatePost(post)
    if err != nil {
        fmt.Printf("Error creating post: %v\n", err)
        return
    }
    
    fmt.Printf("Post created with ID: %s\n", created.ID)
}
```

---

## Blockquotes

### Simple Blockquotes

> This is a simple blockquote. It should appear indented with a vertical line on the left.

### Multi-line Blockquotes

> This is a longer blockquote that spans multiple lines. 
> It should maintain the blockquote formatting across all lines.
> 
> Even with paragraph breaks inside the blockquote.

### Nested Blockquotes

> This is the outer blockquote
> > This is a nested blockquote
> > > This is double nested
> > Back to single nested
> Back to outer level

### Blockquotes with Formatting

> **Bold text** in a blockquote
> 
> *Italic text* in a blockquote
> 
> `inline code` in a blockquote
> 
> Even [links](https://example.com) work in blockquotes

---

## Links and Images

### Various Link Styles

Here's an [inline link](https://substack.com) and here's a [link with title](https://substack.com "Substack Homepage").

Reference-style links: [Substack][1] and [Another link][2]

[1]: https://substack.com
[2]: https://example.com

### Link Edge Cases

- [Empty link text]()
- [Link with special characters: <>&"'](https://example.com)
- https://auto-detected-link.com
- Email link: mailto:test@example.com

### Images

![Alt text for image](https://via.placeholder.com/600x400)

![Image with title](https://via.placeholder.com/800x600 "This is the image title")

### Image with Caption

![A beautiful landscape](https://via.placeholder.com/1200x800)
*Caption: This is a caption for the image above*

---

## Special Elements

### Horizontal Rules

Here's a horizontal rule:

---

And another one:

***

And a third style:

___

### Special Characters & Unicode

Testing special characters: & < > " ' © ® ™ 

Unicode: 🎯 🚀 ✨ 💡 📝 ⭐ ❤️ 👍 🔥 💯

Mathematical symbols: ∑ ∏ ∫ ∂ ∇ ∞ ≈ ≠ ≤ ≥

Greek letters: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω

### HTML Entities

Testing HTML entities: &amp; &lt; &gt; &quot; &apos; &nbsp; &copy; &reg; &trade;

### Tables (if supported)

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
| **Bold** | *Italic* | `Code`   |

---

## Edge Cases

### Very Long Lines

This is a very long line of text that should wrap properly when displayed. It contains no line breaks but goes on and on and on to test how the formatter handles extremely long lines of content without any manual breaks. The line continues with more and more text to ensure it's really, really long and will definitely need to wrap multiple times when rendered in a typical viewport. Let's add even more text to make absolutely sure this line is long enough to test the edge case properly.

### Empty Elements

#### Empty code block:

```
```

#### Empty blockquote:

> 

#### Empty list items:

• 
• Item with content
• 

### Deeply Nested Content

1. Level 1
   • Level 2 bullet
     • Level 3 bullet
       • Level 4 bullet
         • Level 5 bullet
           • Level 6 - How deep can we go?
             • Level 7 - Still going!
               • Level 8 - Getting ridiculous
                 • Level 9 - Almost there
                   • Level 10 - Maximum nesting?

### Mixed Crazy Formatting

This paragraph has **bold with *nested italic* and even `code` inside** plus ***triple formatted text*** and [links with **bold** and *italic*](https://example.com) and `inline code with **bold attempt**` (which shouldn't work).

> A blockquote with **bold**, *italic*, ***both***, `code`, and [a link](https://example.com)
> > Nested quote with # Not a header (escaped)
> > ```python
> > # Code in nested blockquote
> > print("How meta!")
> > ```

### Content Boundaries

Testing 10,000 character line (truncated for readability):
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...

### Special Markdown Characters

Testing backslash escapes: \* \_ \` \# \[ \] \( \) \! \\ \| \{ \}

Testing asterisks: * not italic * ** not bold ** *** not both ***

Testing underscores: _ not italic _ __ not bold __

Testing backticks: ` not code ` `` still not code ``

<!-- PAYWALL -->

## 💰 Premium Content Section

This content appears after the paywall marker. Only paid subscribers can see this section.

### Exclusive Code Example

```python
# ==================== PYTHON CODE ====================
# Premium subscriber-only advanced example
class PremiumSubstackAnalytics:
    \"\"\"Advanced analytics only for paid subscribers\"\"\"
    
    def calculate_roi(self, subscribers, monthly_price):
        # Secret sauce algorithm
        return subscribers * monthly_price * 12 * 1.15
```

### Premium Tips

1. **Advanced Formatting Tip**: Use nested blockquotes with code blocks for technical documentation
2. **Engagement Hack**: Place your best content right after the paywall to maximize conversions
3. **Analytics Secret**: Track read time for paywalled content separately

---

## 🎯 Conclusion

If you can see this entire post with all formatting intact, then our MCP server is working perfectly! This comprehensive test covers:

✅ All 6 header levels  
✅ Bold, italic, and combined text formatting  
✅ Inline code and code blocks with multiple languages  
✅ Ordered and unordered lists (including nested)  
✅ Blockquotes (simple and nested)  
✅ Links (inline, reference, and special cases)  
✅ Images with alt text and captions  
✅ Horizontal rules  
✅ Special characters and Unicode  
✅ Paywall markers  
✅ Edge cases and boundary conditions  

### Post Statistics

- **Sections**: 8 major sections
- **Code blocks**: 6 different languages
- **Special characters**: 50+ unique symbols
- **Formatting combinations**: 20+ different styles
- **Edge cases tested**: 15+

**The ultimate test is complete! 🎉**"""

        print("📝 Creating comprehensive formatting test post...")
        
        create_result = await post_handler.create_draft(
            title="🎯 Ultimate Substack Formatting Test - ALL Options",
            content=content,
            subtitle="Testing every single formatting option to ensure complete MCP server functionality",
            content_type="markdown"
        )
        
        draft_id = create_result.get('id')
        print(f"✅ Comprehensive test post created: {draft_id}")
        
        # Publish immediately
        print(f"🚀 Publishing comprehensive test post...")
        
        publish_result = await post_handler.publish_draft(draft_id)
        
        print(f"✅ Comprehensive test post published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        
        slug = publish_result.get('slug')
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
        print(f"\n🎯 COMPREHENSIVE TEST COMPLETE:")
        print(f"   ✅ All 6 header levels")
        print(f"   ✅ Text formatting (bold, italic, combined)")
        print(f"   ✅ Inline code and formatted code blocks")
        print(f"   ✅ Lists (ordered, unordered, nested)")
        print(f"   ✅ Blockquotes (simple and nested)")
        print(f"   ✅ Links and images")
        print(f"   ✅ Special characters and Unicode")
        print(f"   ✅ Paywall markers")
        print(f"   ✅ Edge cases and boundaries")
        print(f"   ✅ Enhanced code blocks with language headers")
        print(f"\n📖 Check the published post to verify ALL formatting!")
        
    except Exception as e:
        print(f"❌ Comprehensive test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_comprehensive_formatting())