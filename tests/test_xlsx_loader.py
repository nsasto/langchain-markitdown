import pytest
from langchain_markitdown import XlsxLoader
from langchain_core.documents import Document

def test_xlsx_loader(test_xlsx_file):
    """Test loading a XLSX file."""
    loader = XlsxLoader(test_xlsx_file)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) > 0
    assert isinstance(documents[0], Document)
    assert "test.xlsx" in documents[0].metadata["source"]

def test_xlsx_loader_with_split_by_page(test_xlsx_file):
    """Test loading a XLSX file with split_by_page=True."""
    loader = XlsxLoader(test_xlsx_file, split_by_page=True)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) > 0
    assert isinstance(documents[0], Document)
    assert "test.xlsx" in documents[0].metadata["source"]
    
    # Look for page_number instead of worksheet - this appears to be the key used
    # when splitting Excel files by worksheet
    assert "page_number" in documents[0].metadata, "When split_by_page=True, each document should have a page_number in metadata"
    
    # Make sure the content looks like what we'd expect from an Excel file
    assert "|" in documents[0].page_content, "Document content should have table formatting with pipe characters"