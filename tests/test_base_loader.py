import pytest
from langchain_markitdown import BaseMarkitdownLoader


def test_base_loader_file_not_found(fake_converter_factory):
    """Test handling of non-existent file in BaseMarkitdownLoader."""
    loader = BaseMarkitdownLoader(
        "non_existent_file.txt",
        converter=fake_converter_factory(text_content="unused"),
    )
    with pytest.raises(ValueError) as excinfo:
        loader.load()

    assert "Markitdown conversion failed" in str(excinfo.value)
    assert "File not found" in str(excinfo.value)


def test_base_loader_invalid_file(tmp_path, fake_converter_factory):
    """Test handling of an invalid file type with BaseMarkitdownLoader."""
    test_file = tmp_path / "invalid_file.xyz"
    test_file.write_text("data")

    loader = BaseMarkitdownLoader(
        str(test_file),
        converter=fake_converter_factory(exception=RuntimeError("boom")),
    )

    with pytest.raises(ValueError) as excinfo:
        loader.load()

    assert "Markitdown conversion failed" in str(excinfo.value)
    assert "boom" in str(excinfo.value)


def test_base_loader_success_metadata(tmp_path, fake_converter_factory):
    """Ensure successful conversions propagate metadata and content."""
    test_file = tmp_path / "notes.md"
    test_file.write_text("ignored")

    converter = fake_converter_factory(
        text_content="Converted content",
        pages=["section 1"],
        metadata={"producer": "markitdown"},
        attachments=[{"name": "attachment.txt"}],
        format_type="text/markdown",
    )
    loader = BaseMarkitdownLoader(str(test_file), converter=converter)

    documents = loader.load()

    assert len(documents) == 1
    doc = documents[0]

    assert doc.page_content == "Converted content"
    assert doc.metadata["file_name"] == test_file.name
    assert doc.metadata["success"] is True
    assert doc.metadata["conversion_success"] is True
    assert doc.metadata["page_count"] == 1
    assert doc.metadata["attachment_count"] == 1
    assert doc.metadata["markitdown_metadata"] == {"producer": "markitdown"}
