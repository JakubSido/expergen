import pytest
from dataclasses import dataclass
from typing import List
from expergen.dataclass_utils import generate_variations



@dataclass
class NestedClass:
    value: int

@dataclass
class TestClass:
    field1: int
    field2: str
    nested: NestedClass
    list_field: List[int]

def test_generate_variations():
    instance = TestClass(field1=1, field2="test", nested=NestedClass(value=10), list_field=[1, 2, 3])
    
    variations = {
        "field1": [1, 2, 3],
        "nested.value": [10, 20, 30],
        "list_field": [[1, 2, 3], [4, 5, 6]]
    }
    
    results = generate_variations(instance, variations)
    
    assert len(results) == 18  # 3 * 3 * 2 combinations
    assert all(isinstance(r, TestClass) for r in results)
    assert all(r.field1 in [1, 2, 3] for r in results)
    assert all(r.nested.value in [10, 20, 30] for r in results)
    assert all(r.list_field in [[1, 2, 3], [4, 5, 6]] for r in results)

def test_generate_variations_with_transformations():
    instance = TestClass(field1=1, field2="test", nested=NestedClass(value=10), list_field=[1, 2, 3])
    
    variations = {"field1": [1, 2, 3]}
    transformations = {
        "field2": lambda x: x.upper(),
        "nested.value": lambda x: x * 2,
        "list_field": lambda x: [i * 2 for i in x]
    }
    
    results = generate_variations(instance, variations, transformations)
    
    assert len(results) == 3
    assert all(r.field2 == "TEST" for r in results)
    assert all(r.nested.value == 20 for r in results)
    assert all(r.list_field == [2, 4, 6] for r in results)

def test_generate_variations_type_checking():
    instance = TestClass(field1=1, field2="test", nested=NestedClass(value=10), list_field=[1, 2, 3])
    
    variations = {
        "field1": [1, "2", 3],  # "2" is not an int
        "list_field": [[1, 2, 3], [4, "5", 6]]  # "5" is not an int
    }
    
    with pytest.raises(TypeError):
        generate_variations(instance, variations)
