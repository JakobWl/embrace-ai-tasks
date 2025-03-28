from document_parser import parse_document
import json

# Example document
example_text = """
<head>Sample Document</head>
This is a simple document parser example.

<block>
<head>Introduction</head>
This parser can handle various document structures.
</block>

<dict sep=":">
Author: AI Coding Kata
Version: 1.0
</dict>

<list kind=".">
1. Features
1.1. Blocks
1.2. Lists
1.3. Dictionaries
2. Benefits
<list kind="*">
* Easy to use
* Flexible
</list>
</list>
"""

# Parse the document
result = parse_document(example_text)

# Print the result as formatted JSON
print(json.dumps(result.model_dump(), indent=2))