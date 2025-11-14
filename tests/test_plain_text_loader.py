from pathlib import Path

import pytest
from langchain_core.documents import Document

from langchain_markitdown import PlainTextLoader


def test_plain_text_loader(test_text_file, fake_converter_factory):
    """Test loading a plain text file with an injected converter."""
    file_content = Path(test_text_file).read_text(encoding="utf-8")
    loader = PlainTextLoader(
        test_text_file,
        converter=fake_converter_factory(text_content=file_content),
    )

    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.txt" in documents[0].metadata["source"]
    assert file_content == documents[0].page_content
    assert documents[0].metadata["success"] is True
    assert documents[0].metadata["conversion_success"] is True
