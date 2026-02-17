from enum import StrEnum


class URLEnum(StrEnum):
    root = "/"
    id = "/{id}"
    pagination_page = "/pages"
    pagination_limit_offset = "/limit-offset"
    pagination_cursor = "/cursor"

    docs = "/docs"
    static = "/static"
    status = "/status"
    template = "/template"
