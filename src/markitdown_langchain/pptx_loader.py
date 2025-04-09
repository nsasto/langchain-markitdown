from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from src.markitdown_langchain.base_loader import BaseMarkitdownLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.language_models import BaseChatModel
import re
from src.markitdown_langchain.utils import get_image_caption  # Import the function

class PptxLoader(BaseMarkitdownLoader):
    def __init__(self, file_path: str, split_by_page: bool = False, llm: Optional[BaseChatModel] = None):
        super().__init__(file_path)
        self.split_by_page = split_by_page
        self.llm = llm

    def load(
        self, 
        headers_to_split_on: Optional[List[str]] = None
    ) -> List[Document]:
        """Load a PPTX file and convert it to Langchain documents, splitting by Markdown headers."""
        try:
            from markitdown import MarkItDown, MarkitdownConverterOptions
            # Use the imported function for captioning
            converter = MarkItDown(options=MarkitdownConverterOptions(llm_for_image_caption=lambda file_stream, stream_info, **kwargs: get_image_caption(self.llm, file_stream, stream_info) if self.llm else None))
            result = converter.convert(self.file_path)

            metadata: Dict[str, Any] = {
                "source": self.file_path,
                "file_name": self._get_file_name(),
                "file_size": self._get_file_size(),
                "conversion_success": True,
            }

            if result.metadata:
                metadata.update(result.metadata)

            author = result.metadata.get("author")
            if author:
                metadata["author"] = author

            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ] if headers_to_split_on is None else headers_to_split_on

            if self.split_by_page:
                # Split by slide number indicators
                documents = []
                slide_pattern = r"\n\n<!-- Slide number: (\d+) -->\n"
                slide_splits = re.split(slide_pattern, result.text_content)
                
                # The first element will be the content before the first slide indicator
                current_page_content = slide_splits[0]
                current_page_num = 1  # Assume the content before the first indicator belongs to slide 1

                for i in range(1, len(slide_splits), 2):
                    if current_page_content.strip():  # Avoid empty pages
                        page_metadata = metadata.copy()
                        page_metadata["page_number"] = current_page_num
                        
                        # Split page content by headers
                        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                        page_splits = markdown_splitter.split_text(current_page_content)
                        
                        # Add split documents with updated metadata
                        for split in page_splits:
                            split.metadata.update(page_metadata)
                            documents.append(split)

                    current_page_num = int(slide_splits[i])  # Get the slide number from the indicator
                    current_page_content = slide_splits[i + 1]  # Get the content of the current slide

                # Add the last page
                if current_page_content.strip():
                    page_metadata = metadata.copy()
                    page_metadata["page_number"] = current_page_num
                    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                    page_splits = markdown_splitter.split_text(current_page_content)
                    for split in page_splits:
                        split.metadata.update(page_metadata)
                        documents.append(split)
            else:
                # If not splitting by page, perform header-based splitting on the entire document
                markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
                documents = markdown_splitter.split_text(result.text_content)
                for doc in documents:
                    doc.metadata.update(metadata)

            return documents

        except Exception as e:
            raise ValueError(f"Failed to load and convert PPTX file: {e}")
