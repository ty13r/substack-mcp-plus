# Formatting Guide for Substack MCP Plus

This guide demonstrates all the formatting options available when creating posts with Substack MCP Plus. The server accepts Markdown, HTML, or plain text and converts it to Substack's rich text format.

## Table of Contents

1. [Basic Text Formatting](#basic-text-formatting)
2. [Headers](#headers)
3. [Lists](#lists)
4. [Code and Preformatted Text](#code-and-preformatted-text)
5. [Links and Images](#links-and-images)
6. [Blockquotes](#blockquotes)
7. [Horizontal Rules](#horizontal-rules)
8. [Paywall Markers](#paywall-markers)
9. [Complete Example](#complete-example)

## Basic Text Formatting

### Bold Text
```markdown
**This text is bold**
__This is also bold__
```

### Italic Text
```markdown
*This text is italic*
_This is also italic_
```

### Bold and Italic
```markdown
***This text is both bold and italic***
___This is also bold and italic___
```

### Example
```markdown
In this paragraph, we have **bold text**, *italic text*, and ***bold italic text***. 
You can mix and match these styles within a sentence.
```

## Headers

Substack supports six levels of headers:

```markdown
# Header 1 - Main Title
## Header 2 - Section Title
### Header 3 - Subsection
#### Header 4 - Sub-subsection
##### Header 5 - Minor Heading
###### Header 6 - Smallest Heading
```

### Best Practices
- Use Header 1 for the main post title
- Use Header 2 for major sections
- Use Header 3-4 for subsections
- Avoid using Headers 5-6 unless necessary

## Lists

### Unordered Lists (Bullet Points)
```markdown
- First item
- Second item
- Third item
  - Nested item
  - Another nested item
- Back to main level

* You can also use asterisks
* Instead of dashes
+ Or plus signs
```

### Ordered Lists (Numbered)
```markdown
1. First step
2. Second step
3. Third step
   1. Sub-step one
   2. Sub-step two
4. Fourth step
```

### Mixed Lists
```markdown
1. First main point
   - Supporting detail
   - Another detail
2. Second main point
   * Sub-point with asterisk
   * Another sub-point
```

## Code and Preformatted Text

### Inline Code
```markdown
Use `inline code` for short code snippets within text.
```

### Code Blocks with Syntax Highlighting
````markdown
```python
def hello_world():
    """A simple greeting function"""
    print("Hello, Substack readers!")
    return True
```

```javascript
function greetReaders() {
  console.log("Hello from JavaScript!");
  return { success: true };
}
```

```bash
# Install the package
pip install substack-mcp-plus

# Run the server
python -m src.server
```
````

### Supported Languages
- python
- javascript/js
- typescript/ts
- bash/shell
- html
- css
- json
- yaml
- markdown
- sql
- And many more...

## Links and Images

### Links
```markdown
[Visit my website](https://example.com)
[Email me](mailto:hello@example.com)
[Link with title](https://example.com "Hover text")

# Reference-style links
[Link text][1]
[Another link][example]

[1]: https://example.com
[example]: https://example.org
```

### Images
```markdown
![Alt text](https://example.com/image.jpg)
![Alt text with caption](https://example.com/image.jpg "This is a caption")

# Image with link
[![Clickable image](https://example.com/image.jpg)](https://example.com)
```

### Best Practices for Images
- Always include alt text for accessibility
- Use descriptive filenames
- Optimize images before uploading
- Consider using Substack's CDN for better performance

## Blockquotes

```markdown
> This is a blockquote. It's great for highlighting important quotes or callouts.

> Multi-line blockquotes
> can span multiple lines
> like this.

> You can also nest blockquotes
>> This is a nested quote
>>> And even deeper nesting
```

### Blockquote with Attribution
```markdown
> "The best way to predict the future is to invent it."
> 
> — Alan Kay
```

## Horizontal Rules

Use three or more dashes, asterisks, or underscores:

```markdown
---

***

___
```

These create a visual separator between sections.

## Paywall Markers

To separate free and premium content:

```markdown
# Free Content Section

This content is available to all readers...

<!--paywall-->

# Premium Content Section

This content is only for paid subscribers...
```

The `<!--paywall-->` marker tells Substack where to place the paywall.

## Complete Example

Here's a complete post demonstrating various formatting options:

```markdown
# The Ultimate Guide to Python Programming

*Published on November 15, 2024*

Welcome to this comprehensive guide on **Python programming**. Whether you're a ***complete beginner*** or looking to level up your skills, this guide has something for you.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Concepts](#basic-concepts)
3. [Advanced Topics](#advanced-topics)

---

## Getting Started

Before we dive in, let's set up your environment:

```bash
# Install Python
brew install python3

# Verify installation
python3 --version
```

### Why Python?

Python is popular for several reasons:

- **Easy to learn**: Simple, readable syntax
- **Versatile**: Web development, data science, automation
- **Large community**: Extensive libraries and frameworks
- **Cross-platform**: Works on Windows, Mac, and Linux

> "Python is the second best language for everything."
> 
> — Popular programming saying

## Basic Concepts

Let's start with a simple example:

```python
def greet(name):
    """
    A function that greets a person by name.
    
    Args:
        name (str): The person's name
    
    Returns:
        str: A greeting message
    """
    return f"Hello, {name}! Welcome to Python."

# Example usage
message = greet("Reader")
print(message)
```

### Key Features to Remember

1. **Indentation matters** - Python uses whitespace
2. **Dynamic typing** - No need to declare variable types
3. **Everything is an object** - Even functions and classes

<!--paywall-->

## Advanced Topics

*This section is available to paid subscribers only.*

### Decorators

Decorators are a powerful Python feature:

```python
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return "Done!"
```

### Best Practices

- Use `black` for code formatting
- Write comprehensive docstrings
- Follow PEP 8 style guide
- Test your code with `pytest`

---

## Conclusion

Python is an incredible language that opens many doors. Keep practicing, and don't forget to:

- Join the [Python community](https://python.org)
- Read the [official documentation](https://docs.python.org)
- Build projects to solidify your learning

Happy coding! 🐍

![Python Logo](https://example.com/python-logo.png "Python Programming Language")
```

## Working with Images

### Uploading Images

The `upload_image` tool allows you to upload images directly to Substack's CDN:

```python
# Upload from a local file
result = await upload_image(
    source="/path/to/image.jpg",
    optimize_for="web",  # Options: "web", "email", "thumbnail"
    caption="A beautiful sunset"
)

# Upload from a URL
result = await upload_image(
    source="https://example.com/image.jpg",
    optimize_for="email"
)
```

### Image Optimization Options

- **web**: 1456px width, high quality (default)
- **email**: 600px width, optimized for email newsletters
- **thumbnail**: 300px width, lower quality for previews

### Using Images in Posts

Once uploaded, use the CDN URL in your markdown:

```markdown
![Image caption](https://substackcdn.com/image/...)
```

## Tips for Great Formatting

1. **Be Consistent**: Pick a style and stick with it
2. **Use Headers Wisely**: Create a clear hierarchy
3. **Break Up Text**: Use lists, images, and code blocks
4. **Highlight Important Points**: Use bold, italics, and blockquotes
5. **Test Your Formatting**: Preview before publishing
6. **Consider Mobile**: Ensure readability on all devices
7. **Optimize Images**: Use appropriate sizes for different contexts

## Troubleshooting

### Common Issues

1. **Missing line breaks**: Add double line breaks between paragraphs
2. **Code not highlighting**: Ensure you specify the language
3. **Images not showing**: Check URLs are accessible
4. **Lists not formatting**: Ensure proper spacing

### Markdown Variations

Substack supports most CommonMark specifications. If something doesn't work:
- Try alternative syntax (e.g., `*` vs `-` for lists)
- Simplify complex nested structures
- Use HTML as a fallback for advanced formatting