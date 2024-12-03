from dataclasses import asdict, fields, make_dataclass
from itertools import product
from typing import List, Dict, Any, Iterable, Type


def create_dataclass(name: str, field_definitions: Dict[str, type]) -> Type:
    """
    Dynamically create a dataclass.

    :param name: Name of the dataclass.
    :param field_definitions: Dictionary with field names as keys and types as values.
    :return: Dataclass type.
    """
    return make_dataclass(name, [(key, value) for key, value in field_definitions.items()])


def generate_variations(instance: Any, variations: Dict[str, Iterable]) -> List[Any]:
    """
    Generate all variations of the dataclass based on the given parameter iterables.
    
    :param instance: Instance of the dataclass.
    :param variations: Dictionary where keys are field names and values are iterables of possible values.
    :return: List of dataclass instances with all combinations of variations.
    """
    instance_fields = {field.name for field in fields(instance)}
    for var_field in variations.keys():
        if var_field not in instance_fields:
            raise ValueError(f"Field '{var_field}' not found in the dataclass.")

    base_values = asdict(instance)
    keys, iterables = zip(*variations.items())
    combinations = list(product(*iterables))

    results = []
    for combination in combinations:
        updated_values = {**base_values, **dict(zip(keys, combination))}
        results.append(instance.__class__(**updated_values))
    
    return results
