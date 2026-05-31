"""Split document text into overlapping chunks for embedding."""

from typing import List


CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 100   # overlap between adjacent chunks


def chunk_pages(pages: List[str]) -> List[dict]:
    """
    Join all page text, then split into overlapping chunks.

    Args:
        pages: List of page text strings from extract_text_from_pdf

    Returns:
        List of dicts with keys: chunk_index, text
    """
    full_text = "\n\n".join(page for page in pages if page)
    return chunk_text(full_text)


def chunk_text(text: str) -> List[dict]:
    """
    Split a single text string into overlapping chunks.

    Args:
        text: Full document text

    Returns:
        List of dicts with keys: chunk_index, text
    """
    chunks = []
    start = 0
    index = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({"chunk_index": index, "text": chunk})
            index += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
