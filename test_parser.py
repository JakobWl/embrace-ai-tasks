import json
import unittest
from document_parser import parse_document

class TestDocumentParser(unittest.TestCase):
    def assertJsonEqual(self, json1, json2):
        """Compare two JSON objects for structural equality."""
        # Convert both to JSON strings and back to normalize
        self.assertEqual(
            json.loads(json.dumps(json1, sort_keys=True)),
            json.loads(json.dumps(json2, sort_keys=True))
        )

    def test_empty_text(self):
        text = ""
        expected = {
            "kind": "block"
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_body_paragraphs(self):
        text = "First paragraph.\nSecond paragraph."
        expected = {
            "kind": "block",
            "body": [
                "First paragraph.",
                "Second paragraph."
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_body_with_empty_lines(self):
        text = "First paragraph.\n\nSecond paragraph."
        expected = {
            "kind": "block",
            "body": [
                "First paragraph.",
                "Second paragraph."
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_head(self):
        text = "<head>Test Document</head>\nContent"
        expected = {
            "kind": "block",
            "head": "Test Document",
            "body": [
                "Content"
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_nested_blocks(self):
        text = "<head>AI Coding Kata</head>\nLet's get started with the kata\n<block>\n<head>Preface</head>\nHere is a little story\n</block>"
        expected = {
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
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_dictionary(self):
        text = '<dict sep=":">\nKey One: Value One\nKey Two: Value Two\nKey Three: Value Three\n</dict>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "dict",
                    "items": {
                        "Key One": "Value One",
                        "Key Two": "Value Two",
                        "Key Three": "Value Three"
                    }
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_dictionary_with_custom_separator(self):
        text = '<dict sep="-">\nTitle - AI Coding - for TAT\nKata Number - \n</dict>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "dict",
                    "items": {
                        "Title": "AI Coding - for TAT",
                        "Kata Number": ""
                    }
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_ordered_list(self):
        text = '<list kind=".">\n1. First\n2. Second\n</list>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "list",
                    "items": [
                        {"kind": "block", "number": "1.", "head": "First"},
                        {"kind": "block", "number": "2.", "head": "Second"}
                    ]
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_nested_ordered_list(self):
        text = '<list kind=".">\n1. First\n2. Second\n2.1. Subitem 1\n2.2. Subitem 2\n</list>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "list",
                    "items": [
                        {"kind": "block", "number": "1.", "head": "First"},
                        {
                            "kind": "block", 
                            "number": "2.", 
                            "head": "Second", 
                            "body": [
                                {
                                    "kind": "list", 
                                    "items": [
                                        {"kind": "block", "number": "2.1.", "head": "Subitem 1"},
                                        {"kind": "block", "number": "2.2.", "head": "Subitem 2"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_unordered_list(self):
        text = '<list kind="*">\n• First\n• Second\n\n• Third\n</list>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "list",
                    "items": [
                        {"kind": "block", "number": "•", "head": "First"},
                        {"kind": "block", "number": "•", "head": "Second"},
                        {"kind": "block", "number": "•", "head": "Third"}
                    ]
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_nested_unordered_list(self):
        text = '<list kind="*">\n• First\n    o Subitem\n• Second\n• Third\n</list>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "list",
                    "items": [
                        {
                            "kind": "block", 
                            "number": "•", 
                            "head": "First", 
                            "body": [
                                {
                                    "kind": "list", 
                                    "items": [
                                        {"kind": "block", "number": "o", "head": "Subitem"}
                                    ]
                                }
                            ]
                        },
                        {"kind": "block", "number": "•", "head": "Second"},
                        {"kind": "block", "number": "•", "head": "Third"}
                    ]
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_mixed_lists(self):
        text = '<list kind=".">\n1. Beginning\n2. Main \n2.1. Subsection\n<list kind="*">\n* Bullet 1\n* Bullet 2\n</list>\n3. Ending\n</list>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "list",
                    "items": [
                        {"kind": "block", "number": "1.", "head": "Beginning"},
                        {
                            "kind": "block", 
                            "number": "2.", 
                            "head": "Main", 
                            "body": [
                                {
                                    "kind": "list", 
                                    "items": [
                                        {"kind": "block", "number": "*", "head": "Bullet 1"},
                                        {"kind": "block", "number": "*", "head": "Bullet 2"}
                                    ]
                                }
                            ]
                        },
                        {"kind": "block", "number": "2.1.", "head": "Subsection"},
                        {"kind": "block", "number": "3.", "head": "Ending"}
                    ]
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)

    def test_list_with_content(self):
        text = '<list kind=".">\n1. First\nFirst body\n2. Second\nSome more text\n<dict sep=":">\nKey: Value\nAnother Key: Another Value\n</dict>\n</list>'
        expected = {
            "kind": "block",
            "body": [
                {
                    "kind": "list",
                    "items": [
                        {
                            "kind": "block", 
                            "number": "1.", 
                            "head": "First", 
                            "body": [
                                "First body"
                            ]
                        },
                        {
                            "kind": "block", 
                            "number": "2.", 
                            "head": "Second", 
                            "body": [
                                "Some more text",
                                {
                                    "kind": "dict",
                                    "items": {
                                        "Key": "Value",
                                        "Another Key": "Another Value"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        result = parse_document(text).model_dump()
        self.assertJsonEqual(result, expected)


if __name__ == "__main__":
    unittest.main()