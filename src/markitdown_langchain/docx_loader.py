from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from .base_loader import BaseMarkitdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

class DocxLoader(BaseMarkitdownLoader):
    def __init__(self, file_path: str, split_by_page: bool = False):
        super().__init__(file_path)
        self.split_by_page = split_by_page

    def load(
        self,
        headers_to_split_on: Optional[List[str]] = None
    ) -> List[Document]:
        """Load a DOCX file and convert it to Langchain documents, splitting by Markdown headers."""
        try:
            from markitdown import MarkItDown
            converter = MarkItDown()
            result = converter.convert(self.file_path)

            metadata: Dict[str, Any] = {
                "source": self.file_path,
                "file_name": self._get_file_name(self.file_path),
                "file_size": self._get_file_size(self.file_path),
                "conversion_success": True,
            }

            if result.metadata:
                metadata.update(result.metadata)

            author = result.metadata.get("author")
            if author:
                metadata["author"] = author

            if headers_to_split_on is None:
                headers_to_split_on = [
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                ]

            if self.split_by_page:
                # If splitting by page is requested, perform header-based splitting on each page
                documents = []
                if hasattr(result, "pages") and result.pages:
                    for page_num, page_content in enumerate(result.pages, start=1):
                        page_metadata = metadata.copy()
                        page_metadata["page_number"] = page_num

                        # Split page content by headers
                        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                        page_splits = markdown_splitter.split_text(page_content)

                        # Add split documents with updated metadata
                        for split in page_splits:
                            split.metadata.update(page_metadata)  # Add page-level metadata
                            documents.append(split)
                else:
                    # If no page separation info, perform header-based splitting on the entire document
                    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                    documents = markdown_splitter.split_text(result.text_content)
                    for doc in documents:
                        doc.metadata.update(metadata)  # Add document-level metadata
            else:
                # If not splitting by page, perform header-based splitting on the entire document
                markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                documents = markdown_splitter.split_text(result.text_content)
                for doc in documents:
                    doc.metadata.update(metadata)  # Add document-level metadata

            return documents

        except Exception as e:
            raise ValueError(f"Failed to load and convert DOCX file: {e}")
