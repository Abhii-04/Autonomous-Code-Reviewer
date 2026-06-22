from langchain_core.tools import tool

from langchain_community.document_loaders.parsers.language.python import PythonSegmenter
from langchain_community.document_loaders.parsers.language.javascript import JavaScriptSegmenter
from langchain_community.document_loaders.parsers.language.typescript import TypeScriptSegmenter
from langchain_community.document_loaders.parsers.language.c import CSegmenter
from langchain_community.document_loaders.parsers.language.cpp import CPPSegmenter


SEGMENTERS = {
    "py": PythonSegmenter,
    "python": PythonSegmenter,

    "js": JavaScriptSegmenter,
    "javascript": JavaScriptSegmenter,

    "ts": TypeScriptSegmenter,
    "typescript": TypeScriptSegmenter,

    "c": CSegmenter,

    "cpp": CPPSegmenter,
    "cc": CPPSegmenter,
    "cxx": CPPSegmenter,
    "hpp": CPPSegmenter,
}

@tool
def tree_sitter_segmenter(code: str, language: str) -> str:
    """
    Split source code into meaningful functions/classes using Tree-sitter.

    Args:
        code: Full source code as a string.
        language: Programming language or file extension. Example: python, py, js, ts, c, cpp.

    Returns:
        Extracted function/class chunks and simplified code.
    """

    language = language.lower().strip().replace(".", "")

    Segmenter = SEGMENTERS.get(language)

    if Segmenter is None:
        supported = ", ".join(sorted(SEGMENTERS.keys()))
        return f"Unsupported language: {language}. Supported languages: {supported}"

    try:
        segmenter = Segmenter(code)

        if not segmenter.is_valid():
            return "Tree-sitter detected syntax errors in this code."

        chunks = segmenter.extract_functions_classes()
        simplified_code = segmenter.simplify_code()

        if not chunks:
            return f"No functions/classes found.\n\nSimplified code:\n{simplified_code}"

        formatted_chunks = []

        for i, chunk in enumerate(chunks, start=1):
            formatted_chunks.append(f"--- Chunk {i} ---\n{chunk}")

        return (
            "Extracted functions/classes:\n\n"
            + "\n\n".join(formatted_chunks)
            + "\n\n--- Simplified code ---\n"
            + simplified_code
        )

    except Exception as e:
        return f"Tree-sitter segmentation failed: {type(e).__name__}: {e}"