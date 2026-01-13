#!/usr/bin/env python3
"""
Terry-the-Tool-Bot - Advanced AI Coding Assistant Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''

# Read requirements
requirements_file = Path(__file__).parent / 'requirements.txt'
install_requires = []
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        install_requires = [line.strip() for line in f 
                         if line.strip() and not line.startswith('#')]

setup(
    name="terry-tool-bot",
    version="2.0.0",
    author="Terry Development Team",
    author_email="terry@ai-assistant.dev",
    description="Advanced AI coding assistant with Quantum Code Synthesis Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/terry-tool-bot/terry",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
            "sphinx>=5.0",
        ],
        "gui": [
            "pillow>=9.0",
            "customtkinter>=5.0",
        ],
        "qcse": [
            "numpy>=1.21",
            "scipy>=1.7",
            "pymoo>=0.6",
            "numba>=0.56",
            "scikit-learn>=1.1",
        ],
        "enterprise": [
            "redis>=4.0",
            "celery>=5.0",
            "boto3>=1.26",
            "docker>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "terry=main:main",
            "terry-gui=main:main_gui",
        ],
    },
    include_package_data=True,
    package_data={
        "terry": [
            "config/*.yaml",
            "config/themes/*.yaml", 
            "assets/icons/*",
            "assets/sounds/*",
        ],
    },
    zip_safe=False,
    keywords="AI coding assistant android development quantum synthesis",
    project_urls={
        "Bug Reports": "https://github.com/terry-tool-bot/terry/issues",
        "Source": "https://github.com/terry-tool-bot/terry",
        "Documentation": "https://terry-tool-bot.readthedocs.io/",
    },
)