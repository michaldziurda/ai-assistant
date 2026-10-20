import os

def search_files(name:str, start_path=None) -> str:
    if start_path:
        path = start_path
    else:
        path = os.path.abspath(os.sep) # User root directory if not provided
        
    files_found = []
    for root, dirs, files in os.walk(path):
        if name in files:
            files_found.append(os.path.join(root, name))

    if len(files_found) > 0:
        return ",".join(files_found)
    else:
        return ""

SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_files",
        "description": "Search for provided filenames. Optionally provide starting path",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "File name to search for"},
                "start_path": {"type": "string", "description": "Where to begin the search"}
            },
            "required": ["name"]
        }
    }
}