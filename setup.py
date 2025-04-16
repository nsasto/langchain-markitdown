from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='langchain-markitdown',
    version='0.1.5',
    description='LangChain data loaders based on Markdown by @untrueaxioms.',
    author='Nathan Sasto',
    url="https://github.com/nsasto/langchain-markitdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'markitdown[all]',  # Consider specifying a version
        'langchain_core',  # Consider specifying a version
        'langchain-text-splitters',  # Consider specifying a version
        'langchain_openai',  # Consider specifying a version
        'docx'
    ],
    extras_require={
        'dev': [
            'pytest',
            'python-docx',
            'python-pptx',
            'openpyxl',
            'pytest-cov'

        ]
    },
    python_requires='>=3.8',  
    classifiers=[
        'Development Status :: 3 - Alpha',  
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: Markdown',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',  # Adding the SPDX license identifier
)