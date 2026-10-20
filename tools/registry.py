from tools.read_file import read_file, SCHEMA as read_file_schema
from tools.search_files import search_files, SCHEMA as search_files_schema
from tools.system_info import system_info, SCHEMA as system_info_schema

TOOL_REGISTRY = {
    "read_file": read_file,
    "search_files": search_files,
    "system_info": system_info
}

TOOL_SCHEMAS = [read_file_schema, search_files_schema, system_info_schema]