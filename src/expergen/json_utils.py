import os
import json
from typing import List, Type, TypeVar, Union, Any
from pydantic import BaseModel
from dataclasses import asdict, is_dataclass
from dacite import from_dict, Config

T = TypeVar('T', bound=Union[BaseModel, object])

def is_pydantic_model(obj: Any) -> bool:
    return (isinstance(obj, type) and issubclass(obj, BaseModel)) or \
           (hasattr(obj, '__class__') and issubclass(obj.__class__, BaseModel))

def load_from_directory(directory: str, model_type: Type[T]) -> List[T]:
    """
    Load all JSON files from the specified directory and convert them to Pydantic model or dataclass instances.
    
    :param directory: Path to the directory containing JSON files.
    :param model_type: The type to convert the JSON data into (Pydantic model or dataclass).
    :return: List of instances of the specified type.
    """
    instances = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            instance = load_from_json(filepath, model_type)
            instances.append(instance)
    return instances


def save_to_json_files(instances: List[T], destination_dir: str) -> None:
    """
    Save each instance as a separate JSON file in the specified directory.
    Supports both Pydantic models and regular dataclasses.
    
    :param instances: List of instances (Pydantic models or dataclasses).
    :param destination_dir: Path to the directory where files will be saved.
    """
    os.makedirs(destination_dir, exist_ok=True)
    for index, instance in enumerate(instances, start=1):
        filepath = os.path.join(destination_dir, f"instance_{index}.json")
        if is_pydantic_model(instance):
            json_data = instance.model_dump_json(indent=4)
            with open(filepath, 'w') as f:
                f.write(json_data)
        elif is_dataclass(instance):
            with open(filepath, 'w') as f:
                json.dump(asdict(instance), f, indent=4)
        else:
            raise TypeError(f"Instance {index} is neither a Pydantic model nor a dataclass")
    print(f"Saved {len(instances)} files to '{destination_dir}'.")


def load_from_json(filepath: str, model_type: Type[T]) -> T:
    """
    Load a JSON file and convert it to a Pydantic model instance, Pydantic dataclass instance, or a regular dataclass instance.
    
    :param filepath: Path to the JSON file.
    :param model_type: The type to convert the JSON data into (Pydantic model, Pydantic dataclass, or regular dataclass).
    :return: Instance of the specified type.
    """
    with open(filepath, 'r') as f:
        json_data = f.read()
    
    if is_pydantic_model(model_type):
        return model_type.model_validate_json(json_data)
    elif is_dataclass(model_type):
        data = json.loads(json_data)
        return from_dict(data_class=model_type, data=data, config=Config(check_types=True))
    else:
        raise TypeError(f"{model_type} is neither a Pydantic model nor a dataclass")
