<details>

<summary>Firstly pasted the confluence page to gpt 3o to generate file [Confluence.md](Confluence.md)</summary>

<details>
<summary>Prompt</summary>
TimeToAct DocumentAI Spec

Let's define a simple document format that could describe contract, procedure or any other business document in a structured way. It may be used to load this business data into AI Assistants like in ERC.

We’ll work with the documents.

Our documents will consist from blocks. Block is a logical piece of text like pagragraph. It can optionally have a head, number and body. Block body could contain:

    another block

    text

    list

    dictionary

Blocks could contain heterogenous content - texts, other blocks, dictionaries. 

List could contain only similar block items that also have number.
Document Layout

The document below describes a simple text format that could be deterministically parsed into JSON objects. This document is also a test suite! Code admonitions always come in pairs: first input and then json. 

When parser is implemented, parsed input should always produce output that is structurally similar to the expected json. Headline before the code blocks is the name of the text.

Data structures to parse document into could look like this in python:
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
Specifications
Empty text

Empty text results in an empty document block
{
  "kind": "block"
}
Body

Plain text goes into the block body straight away. Different paragraphs are separated by the new lines.
First paragraph.
Second paragraph.

It will be parsed into:
{
  "kind": "block",
  "body": [
    "First paragraph.",
    "Second paragraph."
  ]
}

Note, that we strip and skip empty lines!
First paragraph.

Second paragraph.

results in:
{
  "kind": "block",
  "body": [
    "First paragraph.",
    "Second paragraph."
  ]
}
Head

Text marked with <head> goes directly into the head of the current block.
<head>Test Document</head>
Content
{ "kind": "block",
  "head": "Test Document",
    "body": [
        "Content"
    ]
}
Blocks

You've seen that the document is parsed in a root block. But everything is a block and blocks can be nested explicitly
<head>AI Coding Kata</head>
Let's get started with the kata
<block>
<head>Preface</head>
Here is a little story
</block>

This is how things get extracted:
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
Dictionaries

Dictionaries are used to capture key-value pairs, by default they are separated by ::
<dict sep=":">
Key One: Value One
Key Two: Value Two
Key Three: Value Three
</dict>

this will be parsed into:
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

But we can also have non-standard separator and empty values.
<dict sep="-">
Title - AI Coding - for TAT
Kata Number - 
</dict>
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
Lists

Lists are very important! By default, each non-empty line is a list item. They go inside the root block. There are multiple kinds:

    . for ordered lists that are dot-separated

    * for bulleted lists

Note, that list item goes to head and number goes to number.
Ordered Lists
<list kind=".">
1. First
2. Second
</list>
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number": "1.", "head": "First"  },
        { "kind": "block", "number": "2.", "head":  "Second"  }
      ]
    }
  ]
}

As a convenience, nested lists are automatically detected.
<list kind=".">
1. First
2. Second
2.1. Subitem 1
2.2. Subitem 2    
</list>
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
    
Unordered lists

We can have unordered lists, too:
<list kind="*">
• First
• Second
    
• Third
</list>

They get parsed like this:
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number":"•", "head": "First" },
        { "kind": "block", "number":"•", "head": "Second" },
        { "kind": "block", "number":"•", "head": "Third" }
      ]
    }
  ]
}

And nesting can be done with "o"
<list kind="*">
• First
    o Subitem
• Second
• Third
</list>

this would be loaded as:
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number":"•", "head": "First", "body": [
          { "kind": "list", "items": [
            { "kind": "block", "number":"o", "head": "Subitem" }
          ] }
        ] },
        { "kind": "block", "number":"•", "head": "Second" },
        { "kind": "block", "number":"•", "head": "Third" }
      ]}
    ]}
Mixed lists

We can mix lists, but would need to designate different types separately with tags.
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

this would be parsed into:
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number":"1.", "head": "Beginning" },
        { "kind": "block", "number":"2.", "head": "Main", "body": [
          { "kind": "list", "items": [
            { "kind": "block", "number":"*", "head": "Bullet 1" },
            { "kind": "block", "number":"*", "head": "Bullet 2" }
          ] }
        ] },
        { "kind": "block", "number":"2.1.", "head":  "Subsection" },
        { "kind": "block", "number":"3.",  "head":  "Ending" }
      ]
    }
  ]
}

              
Lists with content

Obviously, lists can have additional content. If something in the current list doesn't match the prefix, then it is treated as block body:
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

it would parse into:
{
  "kind": "block",
  "body": [
    {
      "kind": "list",
      "items": [
        { "kind": "block", "number":"1.", "head": "First", "body": [
          "First body"
        ] },
        { "kind": "block", "number":"2.", "head":  "Second", "body": [
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

this was a confluence page can you make me some markdown of it?
</details>

<details>
<summary>Answer</summary>
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
          ] }
        ] },
        { "kind": "block", "number": "2.1.", "head": "Subsection" },
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

</details>

</details>

<details>
<summary>Then i asked about any bugs in the template</summary>

<details>
<summary>Prompt</summary>
are there any bugs in this document you can find ?
</details>



<details>
<summary>Answer</summary>
</details>
</details>

