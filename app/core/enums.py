from enum import Enum


class SourceType(str, Enum):
    PDF = "pdf"
    WIKI = "wiki"
    DOCS = "docs"