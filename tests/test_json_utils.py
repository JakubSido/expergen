import pytest
import os
import tempfile
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from expergen.json_utils import is_pydantic_model, load_from_directory, save_to_json_files, load_from_json

class PydanticModel(BaseModel):
    field1: int
    field2: str

@dataclass
class DataclassModel:
    field1: int
    field2: str

def test_is_pydantic_model():
    assert is_pydantic_model(PydanticModel)
    assert is_pydantic_model(PydanticModel(field1=1, field2="test"))
    assert not is_pydantic_model(DataclassModel)
    assert not is_pydantic_model(DataclassModel(field1=1, field2="test"))

def test_load_from_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test JSON files
        for i in range(3):
            with open(os.path.join(tmpdir, f"test{i}.json"), "w") as f:
                f.write(f'{{"field1": {i}, "field2": "test{i}"}}')
        
        # Test loading Pydantic models
        pydantic_instances = load_from_directory(tmpdir, PydanticModel)
        assert len(pydantic_instances) == 3
        assert all(isinstance(instance, PydanticModel) for instance in pydantic_instances)
        
        # Test loading dataclass models
        dataclass_instances = load_from_directory(tmpdir, DataclassModel)
        assert len(dataclass_instances) == 3
        assert all(isinstance(instance, DataclassModel) for instance in dataclass_instances)

def test_save_to_json_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        pydantic_instances = [PydanticModel(field1=i, field2=f"test{i}") for i in range(3)]
        dataclass_instances = [DataclassModel(field1=i, field2=f"test{i}") for i in range(3)]
        
        # Test saving Pydantic models
        save_to_json_files(pydantic_instances, os.path.join(tmpdir, "pydantic"))
        assert len(os.listdir(os.path.join(tmpdir, "pydantic"))) == 3
        
        # Test saving dataclass models
        save_to_json_files(dataclass_instances, os.path.join(tmpdir, "dataclass"))
        assert len(os.listdir(os.path.join(tmpdir, "dataclass"))) == 3

def test_load_from_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test JSON file
        json_content = '{"field1": 1, "field2": "test"}'
        filepath = os.path.join(tmpdir, "test.json")
        with open(filepath, "w") as f:
            f.write(json_content)
        
        # Test loading Pydantic model
        pydantic_instance = load_from_json(filepath, PydanticModel)
        assert isinstance(pydantic_instance, PydanticModel)
        assert pydantic_instance.field1 == 1
        assert pydantic_instance.field2 == "test"
        
        # Test loading dataclass model
        dataclass_instance = load_from_json(filepath, DataclassModel)
        assert isinstance(dataclass_instance, DataclassModel)
        assert dataclass_instance.field1 == 1
        assert dataclass_instance.field2 == "test"

def test_load_from_json_invalid_type():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test.json")
        with open(filepath, "w") as f:
            f.write('{"field1": 1, "field2": "test"}')
        
        with pytest.raises(TypeError):
            load_from_json(filepath, List)  # List is neither a Pydantic model nor a dataclass
