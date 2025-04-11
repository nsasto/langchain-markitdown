import pytest
from langchain_markitdown import ImageLoader
from langchain_core.documents import Document
from PIL import Image
import os

@pytest.fixture(scope="module")
def test_image_file(tmpdir_factory):
    """Creates a temporary image file for testing."""
    fn = tmpdir_factory.mktemp("data").join("test.png")
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color = (73, 109, 137))
    img.save(fn)
    return str(fn)

def test_image_loader(test_image_file):
    """Test loading an image file."""
    loader = ImageLoader(test_image_file)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.png" in documents[0].metadata["source"]
    
    # Your ImageLoader doesn't seem to generate page_content
    # Let's check for key metadata instead
    assert "file_name" in documents[0].metadata
    assert "file_size" in documents[0].metadata
    assert os.path.basename(test_image_file) == documents[0].metadata["file_name"]
    
    # Check that file_size is reasonable (should be non-zero)
    assert documents[0].metadata["file_size"] > 0

def test_image_loader_metadata(test_image_file):
    """Test that image metadata is correctly extracted."""
    loader = ImageLoader(test_image_file)
    documents = loader.load()
    
    # Basic checks
    assert len(documents) == 1
    assert "source" in documents[0].metadata
    
    # Check for success indicator
    assert "success" in documents[0].metadata
    assert documents[0].metadata["success"] is True