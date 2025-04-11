import pytest
from langchain_markitdown import BaseMarkitdownLoader
from unittest.mock import patch

def test_base_loader_file_not_found():
    """Test handling of non-existent file in BaseMarkitdownLoader."""
    with pytest.raises(ValueError) as excinfo:
        loader = BaseMarkitdownLoader("non_existent_file.txt")
        loader.load()
    assert "Markitdown conversion failed" in str(excinfo.value)
    assert "File not found" in str(excinfo.value)

def test_base_loader_invalid_file():
    """Test handling of an invalid file type with BaseMarkitdownLoader."""
    with patch("os.path.getsize") as mock_getsize:
        # Mock getsize to avoid FileNotFoundError, so we test the exception from convert
        mock_getsize.return_value = 100
        
        with pytest.raises(ValueError) as excinfo:
            loader = BaseMarkitdownLoader("invalid_file.xyz")
            loader.load()
        
        assert "Markitdown conversion failed" in str(excinfo.value)