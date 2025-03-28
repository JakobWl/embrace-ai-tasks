# TimeToAct DocumentAI Parser

A document parsing system that converts structured text into JSON objects.

## Overview

This parser implements a custom document format that can describe contracts, procedures, or any other business documents in a structured way. The parser converts text into a hierarchical JSON structure, which can be used to load business data into AI Assistants.

## Features

- Parse hierarchical document structures
- Support for nested blocks
- Support for ordered and unordered lists
- Support for dictionaries (key-value pairs)
- Handles mixed content types

## Basic Structure

Documents in this format consist of:

- **Blocks**: Logical pieces of text (like paragraphs) with optional header, number, and body
- **Lists**: Ordered or unordered collections of items
- **Dictionaries**: Key-value pair collections
- **Text**: Plain text paragraphs

## Usage

```python
from document_parser import parse_document

# Parse a document from text
text = """
<head>Sample Document</head>
This is a sample document.

<block>
<head>Introduction</head>
This is the introduction.
</block>

<list kind=".">
1. First item
2. Second item
2.1. Sub-item
</list>
"""

result = parse_document(text)
print(result.model_dump(indent=2))
```

## Testing

To run the tests:

```bash
python -m unittest test_parser.py
```

## Sample Document Format

### Blocks
```
<head>Document Title</head>
Content goes here

<block>
<head>Section Title</head>
Section content goes here
</block>
```

### Dictionaries
```
<dict sep=":">
Key: Value
Another Key: Another Value
</dict>
```

### Lists
```
<list kind=".">
1. First item
2. Second item
   2.1. Sub-item
</list>

<list kind="*">
• First bullet
• Second bullet
  o Sub-bullet
</list>
```

## Data Model

The parser uses Pydantic models to define the document structure:

- `Block`: A general container with optional number, head, and body
- `ListBlock`: A container for list items
- `Dictionary`: A structure for key-value pairs