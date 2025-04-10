from langchain_core.document_loaders import BaseLoader
from typing import List
from langchain_core.documents import Document
import os

class BaseMarkitdownLoader(BaseLoader):
    """Base class for Markitdown document loaders."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:  # Specify return type as List[Document]
        from markitdown import MarkItDown
        metadata = {"source": self.file_path, "success": False}
        try:
            file_name = self._get_file_name(self.file_path)
            metadata["file_name"] = file_name
            file_size = self._get_file_size(self.file_path)
            metadata["file_size"] = file_size
            converter = MarkItDown()
            try:
                markdown_content = converter.convert(self.file_path).text_content
                metadata["success"] = True
                document = Document(page_content=markdown_content, metadata=metadata)
                return [document]
            except Exception as e:
                metadata["success"] = False
                metadata["error"] = str(e)
                raise ValueError(f"Markitdown conversion failed for {self.file_path}: {e}")
        except FileNotFoundError:
            metadata["error"] = "File not found."
            # Adjust the error message to include "Markitdown conversion failed" to match test expectations
            raise ValueError(f"Markitdown conversion failed for {self.file_path}: File not found")
        except Exception as e:
            metadata["error"] = str(e)
            raise ValueError(f"Markitdown conversion failed for {self.file_path}: {e}")

    def _get_file_name(self, file_path: str) -> str:
        """Extract the file name from the file path."""
        return os.path.basename(file_path)

    def _get_file_size(self, file_path: str) -> int:
        """Get the size of the file in bytes."""
        return os.path.getsize(file_path)
