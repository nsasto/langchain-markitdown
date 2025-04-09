from typing import BinaryIO, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
import base64
import mimetypes

def get_image_caption(
    llm: BaseChatModel, file_stream: BinaryIO, stream_info, prompt: Optional[str] = None
) -> Optional[str]:
    """Generates a caption for an image using a Langchain chat model."""

    if prompt is None or prompt.strip() == "":
        prompt = "Write a detailed caption for this image."

    # Get the content type
    content_type = stream_info.mimetype
    if not content_type:
        content_type, _ = mimetypes.guess_type("_dummy" + (stream_info.extension or ""))
    if not content_type:
        content_type = "application/octet-stream"

    # Convert to base64
    cur_pos = file_stream.tell()
    try:
        base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
    except Exception as e:
        return None
    finally:
        file_stream.seek(cur_pos)

    # Prepare the data-uri
    data_uri = f"data:{content_type};base64,{base64_image}"

    # Create a HumanMessage with the image and prompt
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": data_uri},
            },
        ]
    )

    try:
        # Invoke the Langchain model
        response = llm.invoke([message])  # Assuming .invoke() method
        return response.content
    except Exception as e:
        print(f"Error during LLM captioning: {e}")
        return None