"""
Setup script for mcp-m365-teams
"""
from setuptools import setup, find_packages

setup(
    name="mcp-m365-teams",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
)
