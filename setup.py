"""
Setup configuration for hotel-upload-sdk
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="hotel-upload-sdk",
    version="1.0.0",
    author="Finkraft AI",
    author_email="mahesh.dev07@kgrp.in",
    description="Python SDK for hotel data upload with cloud URL validation and duplicate prevention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/finkraftai/hotel-upload-sdk",
    project_urls={
        "Bug Reports": "https://github.com/finkraftai/hotel-upload-sdk/issues",
        "Source": "https://github.com/finkraftai/hotel-upload-sdk",
        "Documentation": "https://github.com/finkraftai/hotel-upload-sdk#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
        ],
    },
    keywords="hotel upload sdk cloud validation s3/azure/cloudfront",
    include_package_data=True,
    zip_safe=False,
)