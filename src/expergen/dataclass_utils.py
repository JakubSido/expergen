from dataclasses import asdict, fields, make_dataclass, is_dataclass
from itertools import product
from typing import List, Dict, Any, Iterable, Type, Callable, Union, get_type_hints


def create_dataclass(name: str, field_definitions: Dict[str, type]) -> Type:
    """
    Dynamically create a dataclass.

    :param name: Name of the dataclass.
    :param field_definitions: Dictionary with field names as keys and types as values.
    :return: Dataclass type.
    """
    return make_dataclass(name, [(key, value) for key, value in field_definitions.items()])


import copy

def generate_variations(instance: Any, variations: Dict[str, Union[Iterable, Dict[str, Iterable]]], transformations: Dict[str, Union[Callable, Dict[str, Callable]]] = None) -> List[Any]:
    """
    Generate all variations of the dataclass based on the given parameter iterables and apply custom transformations.
    Supports nested dataclasses with dot notation.
    
    :param instance: Instance of the dataclass.
    :param variations: Dictionary where keys are field names (with dot notation for nested fields) and values are iterables of possible values.
    :param transformations: Dictionary where keys are field names (with dot notation for nested fields) and values are callable transformations.
    :return: List of dataclass instances with all combinations of variations and transformations applied.
    """
    def get_nested_field(obj, field_path):
        for part in field_path.split('.'):
            if isinstance(obj, dict):
                obj = obj[part]
            else:
                obj = getattr(obj, part)
        return obj

    def set_nested_field(obj, field_path, value):
        parts = field_path.split('.')
        for part in parts[:-1]:
            if isinstance(obj, dict):
                obj = obj[part]
            else:
                obj = getattr(obj, part)
        if isinstance(obj, dict):
            obj[parts[-1]] = value
        else:
            setattr(obj, parts[-1], value)

    def check_type(obj, field_path, value):
        parts = field_path.split('.')
        current_obj = obj
        current_type_hints = get_type_hints(type(obj))
        
        for part in parts:
            if part not in current_type_hints:
                raise ValueError(f"Field '{part}' not found in {type(current_obj).__name__}")
            
            expected_type = current_type_hints[part]
            if is_dataclass(current_obj):
                current_obj = getattr(current_obj, part)
                current_type_hints = get_type_hints(type(current_obj))
            else:
                break
        
        def check_nested_type(value, expected_type):
            if hasattr(expected_type, '__origin__'):
                if expected_type.__origin__ is Union:
                    return any(check_nested_type(value, t) for t in expected_type.__args__)
                elif expected_type.__origin__ is list:
                    if not isinstance(value, list):
                        return False
                    return all(check_nested_type(item, expected_type.__args__[0]) for item in value)
                else:
                    return isinstance(value, expected_type.__origin__)
            else:
                return isinstance(value, expected_type)

        if not check_nested_type(value, expected_type):
            raise TypeError(f"Expected type {expected_type} for field '{field_path}', but got {type(value)}")

    base_values = asdict(instance)
    keys, iterables = zip(*variations.items()) if variations else ([], [])
    combinations = list(product(*iterables)) if iterables else [()]

    results = []
    for combination in combinations:
        new_instance = copy.deepcopy(instance)
        for field, value in zip(keys, combination):
            check_type(new_instance, field, value)
            set_nested_field(new_instance, field, value)
        
        # Apply transformations if provided
        if transformations:
            for field, transform in transformations.items():
                current_value = get_nested_field(new_instance, field)
                new_value = transform(current_value)
                check_type(new_instance, field, new_value)
                set_nested_field(new_instance, field, new_value)
        
        results.append(new_instance)
    
    return results

# This function is no longer needed with the new implementation
