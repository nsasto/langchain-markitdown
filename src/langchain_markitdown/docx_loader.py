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

            # Create basic metadata
            metadata: Dict[str, Any] = {
                "source": self.file_path,
                "file_name": self._get_file_name(self.file_path),
                "file_size": self._get_file_size(self.file_path),
                "conversion_success": True,
            }
            
            # Extract additional metadata directly from the DOCX file using python-docx
            try:
                from docx import Document as DocxDocument
                doc = DocxDocument(self.file_path)
                
                # Extract core properties if available
                core_props = doc.core_properties
                if hasattr(core_props, "author") and core_props.author:
                    metadata["author"] = core_props.author
                if hasattr(core_props, "title") and core_props.title:
                    metadata["title"] = core_props.title
                if hasattr(core_props, "subject") and core_props.subject:
                    metadata["subject"] = core_props.subject
                if hasattr(core_props, "keywords") and core_props.keywords:
                    metadata["keywords"] = core_props.keywords
                if hasattr(core_props, "created") and core_props.created:
                    metadata["created"] = str(core_props.created)
                if hasattr(core_props, "modified") and core_props.modified:
                    metadata["modified"] = str(core_props.modified)
                if hasattr(core_props, "last_modified_by") and core_props.last_modified_by:
                    metadata["last_modified_by"] = core_props.last_modified_by
                if hasattr(core_props, "revision") and core_props.revision:
                    metadata["revision"] = core_props.revision
                if hasattr(core_props, "category") and core_props.category:
                    metadata["category"] = core_props.category
            except Exception as e:  # Catch any exception during metadata extraction
                # If metadata extraction fails, continue with basic metadata
                metadata["metadata_extraction_error"] = str(e)

            # Define default headers to split on if not provided
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

                        # Split page content by headers, keeping the headers in the content
                        markdown_splitter = MarkdownHeaderTextSplitter(
                            headers_to_split_on=headers_to_split_on,
                            return_each_line=True  # This keeps the headers in the content
                        )
                        page_splits = markdown_splitter.split_text(page_content)

                        # Add split documents with updated metadata
                        for split in page_splits:
                            split.metadata.update(page_metadata)  # Add page-level metadata
                            documents.append(split)
                else:
                    # If no page separation info, perform header-based splitting on the entire document
                    markdown_splitter = MarkdownHeaderTextSplitter(
                        headers_to_split_on=headers_to_split_on,
                        return_each_line=True  # This keeps the headers in the content
                    )
                    documents = markdown_splitter.split_text(result.text_content)
                    for doc in documents:
                        doc.metadata.update(metadata)  # Add document-level metadata
            else:
                # If not splitting by page, return a single document with all content
                metadata["content_type"] = "document_full"
                return [Document(page_content=result.text_content, metadata=metadata)]

            return documents

        except Exception as e:
            raise ValueError(f"Failed to load and convert DOCX file: {e}")
