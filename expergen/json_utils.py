import os
import json
from dataclasses import asdict, fields
from typing import List, Any, Type


def save_to_json_files(instances: List[Any], destination_dir: str):
    """
    Save each dataclass instance as a separate JSON file in the specified directory.
    
    :param instances: List of dataclass instances.
    :param destination_dir: Path to the directory where files will be saved.
    """
    os.makedirs(destination_dir, exist_ok=True)
    for index, instance in enumerate(instances, start=1):
        filepath = os.path.join(destination_dir, f"instance_{index}.json")
        with open(filepath, 'w') as file:
            json.dump(asdict(instance), file, indent=4)
    print(f"Saved {len(instances)} files to '{destination_dir}'.")


def load_from_json(filepath: str, dataclass_type: Type) -> List[Any]:
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    results = []
    for item in data:
        field_types = {field.name: field.type for field in fields(dataclass_type)}
        for key, value in item.items():
            if key in field_types:
                expected_type = field_types[key]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Field '{key}' expected {expected_type}, got {type(value)}.")
        
        results.append(dataclass_type(**item))
    
    return results
