import os
import json
import dataclasses
from dataclasses import asdict, fields
from typing import List, Any, Type, TypeVar, get_origin, get_args
from collections.abc import Iterable

T = TypeVar('T')


def load_from_directory(directory: str, dataclass_type: Type[T]) -> List[T]:
    """
    Load all JSON files from the specified directory and convert them to dataclass instances.
    
    :param directory: Path to the directory containing JSON files.
    :param dataclass_type: The type of dataclass to convert the JSON data into.
    :return: List of dataclass instances.
    """
    instances = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            instance = load_from_json(filepath, dataclass_type)
            instances.append(instance)
    return instances


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


def load_from_json(filepath: str, dataclass_type: Type[T]) -> T:
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    def convert_to_dataclass(item, cls):
        if dataclasses.is_dataclass(cls):
            field_types = {f.name: f.type for f in dataclasses.fields(cls)}
            converted_data = {}
            if isinstance(item, dict):
                for key, value in item.items():
                    if key in field_types:
                        converted_data[key] = convert_to_dataclass(value, field_types[key])
                    else:
                        converted_data[key] = value
                return cls(**converted_data)
            else:
                return item
        elif get_origin(cls) is list or (isinstance(cls, type) and issubclass(cls, list)):
            item_type = get_args(cls)[0] if get_args(cls) else Any
            return [convert_to_dataclass(v, item_type) for v in item]
        elif isinstance(item, str):
            return item
        elif isinstance(item, (int, float, bool)):
            return item
        else:
            return item

    return convert_to_dataclass(data, dataclass_type)
