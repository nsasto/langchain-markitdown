# Markitdown LangChain Integration

This project provides document loaders that seamlessly integrate the Markitdown library with LangChain. Markitdown excels at converting various document types (DOCX, PPTX, XLSX, and more) into Markdown format. These loaders empower you to effortlessly load, process, and analyze these documents within your LangChain pipelines.

MarkItDown is a lightweight Python utility designed for converting diverse file formats into Markdown, optimized for use with Large Language Models (LLMs) and related text analysis workflows. It shares similarities with `textract` but distinguishes itself by prioritizing the preservation of crucial document structure and content as Markdown. This includes headings, lists, tables, links, and more. While the output is generally readable, its primary purpose is to be consumed by text analysis tools, rather than serving as a high-fidelity document conversion solution for human readers.

Explore the MarkItDown project on GitHub: [https://github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)

Currently, MarkItDown supports:

- PDF
- PowerPoint
- Word
- Excel
- Images (EXIF metadata and OCR)
- Audio (EXIF metadata and speech transcription)
- HTML
- Text-based formats (CSV, JSON, XML)
- ZIP files (iterates over contents)
- YouTube URLs
- EPUBs
- ...and many more!

While this project borrows liberally from the amazing LangChain and Markitdown projects, it is not affiliated with either in any way.

## Installation

Install the package using pip:

```bash
pip install markitdown-langchain
```

## Usage

### Specific Examples

#### DOCX


```
from markitdown_langchain import DocxLoader

loader = DocxLoader("path/to/your/document.docx")
documents = loader.load()
```

#### PPTX

```
from markitdown_langchain import PptxLoader

loader = PptxLoader("path/to/your/presentation.pptx")
documents = loader.load()
```

#### XLSX


```
from markitdown_langchain import XlsxLoader

loader = XlsxLoader("path/to/your/spreadsheet.xlsx")
documents = loader.load()
```

## Metadata

The `Document` objects returned by the loaders include the following metadata:

- `source`: The path to the source file.
- `file_name`: The name of the source file.
- `file_size`: The size of the source file in bytes.
- `conversion_success`: A boolean indicating whether the conversion to Markdown was successful.
- `author`: The author of the document (if available in the document metadata).
- `page_number`: The page number (if splitting by page).
Header information: When splitting by headers, the metadata will also include the header levels and values for each split.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

[MIT License](LICENSE)

## Trademarks

Markitdown, and so this project by extension, may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft's Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.
