import os

from langchain_core.documents import Document

from langchain_markitdown import ImageLoader


def test_image_loader(test_image_file, fake_converter_factory):
    """Test loading an image file."""
    loader = ImageLoader(
        test_image_file,
        converter=fake_converter_factory(text_content="![alt](image.png)"),
    )
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.png" in documents[0].metadata["source"]
    assert "file_name" in documents[0].metadata
    assert "file_size" in documents[0].metadata
    assert os.path.basename(test_image_file) == documents[0].metadata["file_name"]
    assert documents[0].metadata["file_size"] > 0


def test_image_loader_metadata(test_image_file, fake_converter_factory):
    """Test that image metadata is correctly extracted."""
    loader = ImageLoader(test_image_file, converter=fake_converter_factory(text_content="image"))
    documents = loader.load()

    assert len(documents) == 1
    assert "source" in documents[0].metadata
    assert documents[0].metadata["success"] is True
    assert documents[0].metadata["conversion_success"] is True
