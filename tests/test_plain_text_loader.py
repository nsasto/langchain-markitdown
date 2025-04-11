import pytest
from langchain_markitdown import PlainTextLoader
from langchain_core.documents import Document


def test_plain_text_loader(test_text_file):
    """Test loading a plain text file."""
    loader = PlainTextLoader(test_text_file)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) > 0
    assert isinstance(documents[0], Document)
    assert "test.txt" in documents[0].metadata["source"]
    assert "This is a test file." in documents[0].page_content
