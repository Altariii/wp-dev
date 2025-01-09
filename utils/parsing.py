import json, re
from typing import Callable, Dict, Any

def create_slug(name: str) -> str:
    return re.sub(r'\W+', '-', name).strip('-').lower()

def pascal_case(name: str) -> str:
    words = name.replace('_', ' ').replace('-', ' ').split()
    pascal_case_name = ''.join(word.capitalize() for word in words)

    return pascal_case_name

def fix_json_file(path: str, modify_func: Callable[[Dict[str, Any]], None] = None) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    try:
        json_content = json.loads(content)
    except json.JSONDecodeError as e:
        return
    
    if modify_func:
        modify_func(json_content)
    
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, indent=4, ensure_ascii=False)