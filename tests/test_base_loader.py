import pytest
from langchain_markitdown import BaseMarkitdownLoader
from unittest.mock import patch

def test_base_loader_file_not_found():
    """Test handling of non-existent file in BaseMarkitdownLoader."""
    with pytest.raises(ValueError) as excinfo:
        BaseMarkitdownLoader("non_existent_file.txt").load()
    assert "Markitdown conversion failed" in str(excinfo.value)
    assert "File not found" in str(excinfo.value)

def test_base_loader_invalid_file():
    """Test handling of an invalid file type with BaseMarkitdownLoader."""
    with patch("os.path.getsize") as mock_getsize, pytest.raises(ValueError) as excinfo:
        mock_getsize.side_effect = FileNotFoundError
        loader = BaseMarkitdownLoader("invalid_file.xyz")
        loader.load()
    assert "Markitdown conversion failed" in str(excinfo.value)