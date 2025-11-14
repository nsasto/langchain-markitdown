from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

install_requires = [
    "markitdown[all]>=0.1.3",
    "langchain-core>=1.0.4",
    "langchain-text-splitters>=1.0.0",
    "langchain-openai>=1.0.2",
    "python-docx>=1.2.0",
    "pillow>=12.0.0",
]

setup(
    name="langchain-markitdown",
    version="1.0.0",
    description="LangChain data loaders based on Markdown by @untrueaxioms.",
    author="Nathan Sasto",
    url="https://github.com/nsasto/langchain-markitdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    extras_require={
        "dev": ["pytest", "python-docx", "python-pptx", "openpyxl", "pytest-cov"]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",  # Adding the SPDX license identifier
)
