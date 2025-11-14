from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

if TYPE_CHECKING:
    from markitdown import MarkItDown

module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.WARNING)

if not module_logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    handler.setFormatter(formatter)
    module_logger.addHandler(handler)


class BaseMarkitdownLoader(BaseLoader):
    """Base class for MarkItDown document loaders."""

    def __init__(
        self,
        file_path: str,
        verbose: bool = False,
        *,
        converter: Optional["MarkItDown"] = None,
    ):
        self.file_path = file_path
        self._converter = converter

        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        if verbose:
            self.logger.setLevel(logging.INFO)

        self.logger.info("Initialized %s for %s", self.__class__.__name__, file_path)

    def load(self) -> List[Document]:
        """Convert the target file into a single LangChain document."""
        metadata: Dict[str, Any] = {
            "source": self.file_path,
            "success": False,
            "conversion_success": False,
        }

        try:
            metadata.update(self._file_metadata())
            result = self._convert_to_markdown()
            metadata["success"] = True
            metadata["conversion_success"] = True
            metadata.update(self._extract_conversion_metadata(result))

            page_content = self._get_text_content(result)
            return [Document(page_content=page_content, metadata=metadata)]
        except FileNotFoundError as exc:
            metadata["error"] = "File not found."
            raise ValueError(
                f"Markitdown conversion failed for {self.file_path}: File not found",
            ) from exc
        except Exception as exc:
            metadata["error"] = str(exc)
            raise ValueError(
                f"Markitdown conversion failed for {self.file_path}: {exc}",
            ) from exc

    def _convert_to_markdown(self) -> Any:
        """Convert the source file to markdown using MarkItDown."""
        if self._converter is None:
            from markitdown import MarkItDown

            self._converter = MarkItDown()

        return self._converter.convert(self.file_path)

    def _file_metadata(self) -> Dict[str, Any]:
        """Return base metadata for the current file."""
        return {
            "file_name": self._get_file_name(self.file_path),
            "file_size": self._get_file_size(self.file_path),
        }

    def _extract_conversion_metadata(self, result: Any) -> Dict[str, Any]:
        """Collect metadata surfaced by MarkItDown's conversion result."""
        metadata: Dict[str, Any] = {}

        markitdown_metadata = getattr(result, "metadata", None)
        if isinstance(markitdown_metadata, dict) and markitdown_metadata:
            metadata["markitdown_metadata"] = markitdown_metadata

        pages = getattr(result, "pages", None)
        if isinstance(pages, list):
            metadata["page_count"] = len(pages)

        attachments = getattr(result, "attachments", None)
        if isinstance(attachments, list) and attachments:
            metadata["attachment_count"] = len(attachments)

        output_type = getattr(result, "output_type", None)
        if output_type:
            metadata["conversion_output_type"] = output_type

        format_type = getattr(result, "format_type", None)
        if format_type:
            metadata["document_type"] = format_type

        return metadata

    def _get_text_content(self, result: Any) -> str:
        """Normalize the text content returned by MarkItDown."""
        content = getattr(result, "text_content", "") or ""
        return content

    def _get_file_name(self, file_path: str) -> str:
        """Extract the file name from the file path."""
        return os.path.basename(file_path)

    def _get_file_size(self, file_path: str) -> int:
        """Get the size of the file in bytes."""
        return os.path.getsize(file_path)
