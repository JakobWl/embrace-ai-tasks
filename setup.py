from setuptools import setup, find_packages

setup(
    name="document_parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
    ],
    description="A document parsing system that converts structured text into JSON objects",
    author="AI Coding Kata",
)