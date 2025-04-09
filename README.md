# Markitdown LangChain Integration

This project provides document loaders that integrate the Markitdown library with LangChain. Markitdown allows for converting various document types (DOCX, PPTX, XLSX, and more) to Markdown, and these loaders enable you to easily load and process those documents within a LangChain pipeline.

MarkItDown is a lightweight Python utility for converting various files to Markdown for use with LLMs and related text analysis pipelines. To this end, it is most comparable to textract, but with a focus on preserving important document structure and content as Markdown (including: headings, lists, tables, links, etc.) While the output is often reasonably presentable and human-friendly, it is meant to be consumed by text analysis tools -- and may not be the best option for high-fidelity document conversions for human consumption.

You can find the project (on github here)[https://github.com/microsoft/markitdown]

At present, MarkItDown supports:

PDF
PowerPoint
Word
Excel
Images (EXIF metadata and OCR)
Audio (EXIF metadata and speech transcription)
HTML
Text-based formats (CSV, JSON, XML)
ZIP files (iterates over contents)
Youtube URLs
EPubs
... and more!

## Installation

To install the package, use pip:


bash pip install markitdown-langchain

## Usage

### General Example

The loaders can be used to load any supported file type. Here's a general example:


python from markitdown_langchain import # Replace with the specific loader you need from langchain_core.prompts import ChatPromptTemplate from langchain_core.output_parsers import StrOutputParser from langchain_core.runnables import RunnablePassthrough from langchain_openai import ChatOpenAI

loader = # Replace with the specific loader (e.g., DocxLoader, PptxLoader, etc.) documents = loader.load()

template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.

Question: {question} Context: {context} Answer:""" prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def format_docs(docs): return "\n\n".join(doc.page_content for doc in docs)

rag_chain = ( {"context": documents | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser() )

question = "What is the main topic of this document?" answer = rag_chain.invoke(question) print(answer)

### Specific Examples

#### DOCX


python from markitdown_langchain import DocxLoader

loader = DocxLoader("path/to/your/document.docx") documents = loader.load()

#### PPTX


python from markitdown_langchain import PptxLoader

loader = PptxLoader("path/to/your/presentation.pptx") documents = loader.load()

#### XLSX


python from markitdown_langchain import XlsxLoader

loader = XlsxLoader("path/to/your/spreadsheet.xlsx") documents = loader.load()

## Metadata

The `Document` objects returned by the loaders include the following metadata:

*   `source`: The path to the source file.
*   `file_name`: The name of the source file.
*   `file_size`: The size of the source file in bytes.
*   `conversion_success`: A boolean indicating whether the conversion to Markdown was successful.
*   `author`: The author of the document (if available in the document metadata).
*   `page_number`: The page number (if splitting by page).
*   Header information: When splitting by headers, the metadata will also include the header levels and values for each split.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

[MIT License](LICENSE)

## Trademarks

Markitdown, and so this project by extension, may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft's Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.
