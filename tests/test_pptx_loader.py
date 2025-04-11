import pytest
from langchain_markitdown import PptxLoader
from langchain_core.documents import Document

def test_pptx_loader(test_pptx_file):
    """Test loading a PPTX file."""
    loader = PptxLoader(test_pptx_file)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) > 0
    assert isinstance(documents[0], Document)
    assert "test.pptx" in documents[0].metadata["source"]

def test_pptx_loader_with_split_by_page(test_pptx_file):
    """Test loading a PPTX file with split_by_page=True."""
    loader = PptxLoader(test_pptx_file, split_by_page=True)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) > 0
    assert isinstance(documents[0], Document)
    assert "test.pptx" in documents[0].metadata["source"]
    assert "page_number" in documents[0].metadata