ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "image/png",
    "image/jpeg",
    "image/webp",
}


def is_allowed_content_type(content_type: str | None) -> bool:
    return bool(content_type) and content_type.lower() in ALLOWED_CONTENT_TYPES
