from document_parser import parse_document, Block, ListBlock, Dictionary
import json
import sys

# Test cases from the specification
test_cases = [
    {
        "name": "Empty text",
        "input": "",
        "expected": {
            "kind": "block"
        }
    },
    {
        "name": "Body paragraphs",
        "input": "First paragraph.\nSecond paragraph.",
        "expected": {
            "kind": "block",
            "body": [
                "First paragraph.",
                "Second paragraph."
            ]
        }
    },
    {
        "name": "Body with empty lines",
        "input": "First paragraph.\n\nSecond paragraph.",
        "expected": {
            "kind": "block",
            "body": [
                "First paragraph.",
                "Second paragraph."
            ]
        }
    },
    {
        "name": "Head tag",
        "input": "<head>Test Document</head>\nContent",
        "expected": {
            "kind": "block",
            "head": "Test Document",
            "body": [
                "Content"
            ]
        }
    },
    {
        "name": "Nested blocks",
        "input": "<head>AI Coding Kata</head>\nLet's get started with the kata\n<block>\n<head>Preface</head>\nHere is a little story\n</block>",
        "expected": {
            "kind": "block",
            "head": "AI Coding Kata",
            "body": [
                "Let's get started with the kata",
                {
                    "kind": "block",
                    "head": "Preface",
                    "body": [
                        "Here is a little story"
                    ]
                }
            ]
        }
    }
]

# Run tests
print("Running manual tests...")
for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['name']}")
    
    try:
        # Handle different Pydantic versions
        result = parse_document(test["input"])
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result.dict()
        
        # Compare with expected output
        expected_json = json.dumps(test["expected"], sort_keys=True, indent=2)
        result_json = json.dumps(result_dict, sort_keys=True, indent=2)
        
        if expected_json == result_json:
            print(f"PASS")
        else:
            print(f"FAIL")
            print(f"\nExpected:\n{expected_json}")
            print(f"\nGot:\n{result_json}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

# Test with a more complex document
complex_doc = """
<head>Complex Document</head>
This tests multiple features together.

<block>
<head>Section One</head>
This is the first section.

<dict sep=":">
Key 1: Value 1
Key 2: Value with : colon
</dict>
</block>

<list kind=".">
1. First item
   First item content
2. Second item
   <dict sep="-">
   Name - John Doe
   Title - Developer
   </dict>
   
   <list kind="*">
   • Sub bullet A
   • Sub bullet B
     o Nested bullet
   </list>
</list>
"""

print("\n\nTesting complex document:")
try:
    result = parse_document(complex_doc)
    # Handle different Pydantic versions
    if hasattr(result, "model_dump"):
        result_dict = result.model_dump()
    else:
        result_dict = result.dict()
    
    print(json.dumps(result_dict, indent=2))
    print("\nComplex document parsed successfully")
except Exception as e:
    print(f"ERROR parsing complex document: {str(e)}")