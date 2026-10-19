def read_file(file_path:str) -> str:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return content
    except FileNotFoundError as e:
        return f"File doesn't exist in the specified location"
    
