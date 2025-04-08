Below is a Markdown version of your TimeToAct DocumentAI Spec that you can copy into a Markdown file. It includes all the details, sections, and examples as described in your Confluence page.

---

# TimeToAct DocumentAI Spec

Let's define a simple document format that can describe a contract, procedure, or any other business document in a structured way. This format can be used to load business data into AI Assistants (as in ERC).

Our documents are built from **blocks**. A block is a logical piece of text (like a paragraph). Each block can optionally have:
- **head**
- **number**
- **body**

A block's body may contain:
- Another block
- Plain text
- A list
- A dictionary

> **Note:** Blocks can have heterogeneous content (texts, other blocks, dictionaries), while lists are composed of similar block items that also have a number.

---

## Document Layout

The document below describes a simple text format that can be deterministically parsed into JSON objects. This document also acts as a test suite, where code admonitions always come in pairs (first the input and then the expected JSON output).

---

## Python Data Structures

The following Python code shows one way to define the data structures for parsing the document into JSON using [Pydantic](https://pydantic-docs.helpmanual.io/):

```python
from typing import List, Optional, Union, Dict, Literal
from pydantic import BaseModel, Field

# This type alias helps with readability and forward references.
ContentNode = Union[str, "Block", "ListBlock", "Dictionary"]

class Dictionary(BaseModel):
    """
    A distinct dictionary structure for key-value pairs.
    """
    kind: Literal["dict"]
    items: Dict[str, str] = Field(default_factory=dict)

class Block(BaseModel):
    """
    A general-purpose container for a 'section' or item.
    
    - 'number' can store a section number (e.g., "5", "5.1") if applicable.
    - 'head' is an optional heading for the block.
    - 'body' can hold any mix of strings, sub-blocks, dictionaries, or lists.
    """
    kind: Literal["block"]
    number: Optional[str] = None
    head: Optional[str] = None
    body: List[ContentNode] = Field(default_factory=list)

class ListBlock(BaseModel):
    """
    A container for a list of items, each item being a 'Block'.
    """
    kind: Literal["list"]
    items: List[Block] = Field(default_factory=list)

# Important for forward references within union types
Block.model_rebuild()
```

---

## Specifications

### 1. Empty Text

Empty text results in an empty document block.

**Input (empty text):**

```
(empty)
```

**Output:**

```json
{
  "kind": "block"
}
```

---

### 2. Body (Plain Text)

Plain text is placed directly into the block's body. Different paragraphs are separated by new lines.

**Input:**

```
First paragraph.
Second paragraph.
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    "First paragraph.",
    "Second paragraph."
  ]
}
```

> **Note:** Empty lines are stripped and skipped. For example, the input below:
>
> ```
> First paragraph.
>
> Second paragraph.
> ```
>
> still produces the same output.

---

### 3. Head

Text marked with `<head>` is extracted into the block's head.

**Input:**

```
<head>Test Document</head>
Content
```

**Output:**

```json
{
  "kind": "block",
  "head": "Test Document",
  "body": [
    "Content"
  ]
}
```

---

### 4. Blocks

Everything is a block, and blocks can be nested explicitly.

**Input:**

```
<head>AI Coding Kata</head>
Let's get started with the kata
<block>
<head>Preface</head>
Here is a little story
</block>
```

**Output:**

```json
{
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
```

---

### 5. Dictionaries

Dictionaries capture key-value pairs. By default, the keys and values are separated by the designated separator (`sep` attribute).

#### Example with Standard Separator (`:`)

**Input:**

```
<dict sep=":">
Key One: Value One
Key Two: Value Two
Key Three: Value Three
</dict>
```

**Output:**

```json
{
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
```

#### Example with a Non-standard Separator (`-`) and Empty Value

**Input:**

```
<dict sep="-">
Title - AI Coding - for TAT
Kata Number - 
</dict>
```

**Output:**

```json
{
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
```

---

### 6. Lists

Lists can be of different types and are contained within the document's root block.

#### 6.1 Ordered Lists

Ordered lists use a dot (`.`) as the separator. The list item number goes into the block's number, and the text becomes the head.

**Example:**

**Input:**

```
<list kind=".">
1. First
2. Second
</list>
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "1.", "head": "First" },
        { "kind": "block", "number": "2.", "head": "Second" }
      ]
    }
  ]
}
```

_Nested Ordered Lists:_

**Input:**

```
<list kind=".">
1. First
2. Second
2.1. Subitem 1
2.2. Subitem 2    
</list>
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "1.", "head": "First" },
        { "kind": "block", "number": "2.", "head": "Second", "body": [ 
          { "kind": "list", "items": [ 
            { "kind": "block", "number": "2.1.", "head": "Subitem 1" }, 
            { "kind": "block", "number": "2.2.", "head": "Subitem 2" } 
          ] } 
        ] }
      ]
    }
  ]
}
```

---

#### 6.2 Unordered Lists

Unordered lists use symbols (like `•`) to denote items. These symbols go into the block's number, with the text in the head.

**Example:**

**Input:**

```
<list kind="*">
• First
• Second

• Third
</list>
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "•", "head": "First" },
        { "kind": "block", "number": "•", "head": "Second" },
        { "kind": "block", "number": "•", "head": "Third" }
      ]
    }
  ]
}
```

_Nested Unordered Lists:_

**Input:**

```
<list kind="*">
• First
    o Subitem
• Second
• Third
</list>
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "•", "head": "First", "body": [
          { "kind": "list", "items": [
            { "kind": "block", "number": "o", "head": "Subitem" }
          ] }
        ] },
        { "kind": "block", "number": "•", "head": "Second" },
        { "kind": "block", "number": "•", "head": "Third" }
      ]
    }
  ]
}
```

---

#### 6.3 Mixed Lists

Mixed lists allow combining different types of lists. Different list types must be designated with separate tags.

**Input:**

```
<list kind=".">
1. Beginning
2. Main 
2.1. Subsection
<list kind="*">
* Bullet 1
* Bullet 2
</list>
3. Ending
</list>
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "1.", "head": "Beginning" },
        { "kind": "block", "number": "2.", "head": "Main", "body": [
          { "kind": "list", "items": [
            { "kind": "block", "number": "*", "head": "Bullet 1" },
            { "kind": "block", "number": "*", "head": "Bullet 2" }
          ] },
          { "kind": "block", "number": "2.1.", "head": "Subsection" }
        ] },
        { "kind": "block", "number": "3.", "head": "Ending" }
      ]
    }
  ]
}
```

---

### 7. Lists with Additional Content

List items can include additional content. Lines that do not match the list item prefix are treated as part of the block body.

**Input:**

```
<list kind=".">
1. First
First body
2. Second
Some more text
<dict sep=":">
Key: Value
Another Key: Another Value
</dict>
</list>
```

**Output:**

```json
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "1.", "head": "First", "body": [
          "First body"
        ] },
        { "kind": "block", "number": "2.", "head": "Second", "body": [
          "Some more text",
          {
            "kind": "dict",
            "items": {
              "Key": "Value",
              "Another Key": "Another Value"
            }
          }
        ] }
      ]
    }
  ]
}
```

---

This Markdown file serves as both a specification and a test suite for the TimeToAct DocumentAI parser. You can extend or modify this as needed for your specific use case.