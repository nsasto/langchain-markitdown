from setuptools import setup, find_packages

setup(
    name='markitdown-langchain',
    version='0.1.0',
    description='LangChain data loaders based on Markdown.',
    author='Nathan Sasto',
    author_email='nathan@decisiondecoder.net',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['markitdown[all]', 'langchain_core', 'langchain-text-splitters', 'langchain_openai']
)