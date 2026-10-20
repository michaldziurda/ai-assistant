import os
import fnmatch

def search_files(pattern:str, start_path=None) -> str:
    path = start_path or os.path.abspath(os.sep) # If path not provided, use root dir
        
    files_found = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                files_found.append(os.path.join(root, f))

    if len(files_found) > 0:
        return "\n".join(files_found)
    else:
        return f"No files found matching {pattern} found in {path}"

SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_files",
        "description": "Search for files matching a glob pattern. Optionally provide starting path",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern, e.g. *.json, *.py, report_*"},
                "start_path": {"type": "string", "description": "Directory to search in"}
            },
            "required": ["pattern"]
        }
    }
}