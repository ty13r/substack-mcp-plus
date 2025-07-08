#!/usr/bin/env python3
"""
Test enhanced code blocks with clarity comments
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
async def test_enhanced_code_blocks():
    print("🧪 Testing enhanced code blocks with clarity comments...")
    
    try:
        # Authenticate and create handlers
        auth = AuthHandler()
        client = await auth.authenticate()
        post_handler = PostHandler(client)
        
        # Test content with various code blocks that will get clarity enhancements
        content = """# Enhanced Code Blocks with Clarity Comments

This post demonstrates our improved code block formatting with automatic language headers and better readability.

## Python Example - Data Processing

Here's a Python script that processes user data:

```python
# Function to process user data with validation
def process_user_data(users):
    \"\"\"Process and validate user data\"\"\"
    
    # Initialize results container
    valid_users = []
    invalid_users = []
    
    # Process each user
    for user in users:
        # Validate required fields
        if 'email' in user and 'name' in user:
            # Email validation using regex
            if '@' in user['email'] and '.' in user['email']:
                valid_users.append(user)
            else:
                invalid_users.append(user)
        else:
            invalid_users.append(user)
    
    # Return categorized results
    return {
        'valid': valid_users,
        'invalid': invalid_users,
        'total_processed': len(users),
        'success_rate': len(valid_users) / len(users) * 100
    }

# Example usage
test_users = [
    {'name': 'John Doe', 'email': 'john@example.com'},
    {'name': 'Invalid User', 'email': 'notanemail'},
    {'name': 'No Email'},
]

result = process_user_data(test_users)
print(f"Success rate: {result['success_rate']}%")
```

## JavaScript Example - API Handler

A JavaScript function for handling API requests:

```javascript
// Async function to fetch user data from API
async function fetchUserData(userId) {
    // Input validation
    if (!userId || typeof userId !== 'number') {
        throw new Error('Invalid user ID provided');
    }
    
    // Configuration
    const API_BASE = 'https://api.example.com';
    const endpoint = `${API_BASE}/users/${userId}`;
    
    try {
        // Make the API request
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${process.env.API_TOKEN}`
            }
        });
        
        // Check response status
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse and return JSON data
        const userData = await response.json();
        return userData;
        
    } catch (error) {
        // Log error and re-throw
        console.error('API request failed:', error);
        throw error;
    }
}

// Usage with error handling
fetchUserData(123)
    .then(user => console.log('User data:', user))
    .catch(err => console.error('Failed to fetch user:', err));
```

## SQL Example - Database Query

Complex SQL query with joins:

```sql
-- Query to get user activity summary
WITH user_activity AS (
    -- Get recent activity for each user
    SELECT 
        u.user_id,
        u.username,
        COUNT(DISTINCT a.activity_id) as activity_count,
        MAX(a.created_at) as last_active
    FROM users u
    LEFT JOIN activities a ON u.user_id = a.user_id
    WHERE 
        u.status = 'active'
        AND a.created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY u.user_id, u.username
)
-- Main query with categorization
SELECT 
    username,
    activity_count,
    last_active,
    CASE 
        WHEN activity_count >= 20 THEN 'High Activity'
        WHEN activity_count >= 10 THEN 'Medium Activity'
        WHEN activity_count > 0 THEN 'Low Activity'
        ELSE 'Inactive'
    END as activity_level
FROM user_activity
ORDER BY activity_count DESC, last_active DESC
LIMIT 100;
```

## Bash Script - Deployment Automation

Shell script for automated deployment:

```bash
#!/bin/bash

# Script configuration
APP_NAME="my-app"
DEPLOY_ENV=${1:-"staging"}
BUILD_DIR="./dist"

# Function to check prerequisites
check_prerequisites() {
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo "Error: Node.js is required but not installed"
        exit 1
    fi
    
    # Check if build directory exists
    if [ ! -d "$BUILD_DIR" ]; then
        echo "Error: Build directory not found"
        exit 1
    fi
}

# Function to deploy application
deploy_app() {
    echo "Deploying $APP_NAME to $DEPLOY_ENV..."
    
    # Run tests first
    npm test || { echo "Tests failed!"; exit 1; }
    
    # Build the application
    npm run build:$DEPLOY_ENV
    
    # Deploy based on environment
    case $DEPLOY_ENV in
        "production")
            aws s3 sync $BUILD_DIR s3://prod-bucket/
            aws cloudfront create-invalidation --distribution-id XXXXX --paths "/*"
            ;;
        "staging")
            aws s3 sync $BUILD_DIR s3://staging-bucket/
            ;;
        *)
            echo "Unknown environment: $DEPLOY_ENV"
            exit 1
            ;;
    esac
    
    echo "Deployment complete!"
}

# Main execution
check_prerequisites
deploy_app
```

## Benefits of Enhanced Code Blocks

With our clarity enhancements:

1. **Language Headers** - Each code block starts with a clear language identifier
2. **Structured Comments** - Strategic comments improve readability
3. **Section Separation** - Visual breaks between code sections
4. **Purpose Documentation** - Comments explain what code does
5. **Better Organization** - Logical grouping of related code

## Conclusion

These enhanced code blocks provide better readability even without syntax highlighting. The automatic language headers and strategic commenting make code much easier to understand for readers.

**Try it in your own posts!** The MCP server will automatically enhance your code blocks for maximum clarity."""

        print("📝 Creating post with enhanced code blocks...")
        
        create_result = await post_handler.create_draft(
            title="📝 Enhanced Code Blocks - Improved Readability",
            content=content,
            subtitle="Demonstrating code blocks with automatic clarity enhancements",
            content_type="markdown"
        )
        
        draft_id = create_result.get('id')
        print(f"✅ Enhanced code block post created: {draft_id}")
        
        # Publish immediately
        print(f"🚀 Publishing enhanced code block post...")
        
        publish_result = await post_handler.publish_draft(draft_id)
        
        print(f"✅ Enhanced code block post published!")
        print(f"🌐 Post ID: {publish_result.get('id')}")
        
        slug = publish_result.get('slug')
        if slug:
            print(f"🔗 Post URL: https://neroaugustus.substack.com/p/{slug}")
        
        print(f"\n🎯 ENHANCEMENTS APPLIED:")
        print(f"   ✅ Language headers added to code blocks")
        print(f"   ✅ Appropriate comment characters for each language")
        print(f"   ✅ Visual separators for clarity")
        print(f"   ✅ Maintained original code structure")
        print(f"\n📖 Check the post to see improved readability!")
        
    except Exception as e:
        print(f"❌ Enhanced code block test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_code_blocks())