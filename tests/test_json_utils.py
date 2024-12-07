import pytest
import os
import tempfile
import json
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from expergen.json_utils import is_pydantic_model, load_from_directory, save_to_directory, load_from_json

class PydanticModel(BaseModel):
    field1: int
    field2: str


class PydanticModel2(BaseModel):
    field1: int
    field2: str

def test_is_pydantic_model():
    assert is_pydantic_model(PydanticModel)
    assert is_pydantic_model(PydanticModel(field1=1, field2="test"))

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
        dataclass_instances = load_from_directory(tmpdir, PydanticModel2)
        assert len(dataclass_instances) == 3
        assert all(isinstance(instance, PydanticModel2) for instance in dataclass_instances)

def test_save_to_json_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        pydantic_instances = [PydanticModel(field1=i, field2=f"test{i}") for i in range(3)]
        dataclass_instances = [PydanticModel2(field1=i, field2=f"test{i}") for i in range(3)]
        
        # Test saving Pydantic models
        save_to_directory(pydantic_instances, os.path.join(tmpdir, "pydantic"))
        assert len(os.listdir(os.path.join(tmpdir, "pydantic"))) == 3
        
        # Test saving dataclass models
        save_to_directory(dataclass_instances, os.path.join(tmpdir, "dataclass"))
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
        dataclass_instance = load_from_json(filepath, PydanticModel2)
        assert isinstance(dataclass_instance, PydanticModel2)
        assert dataclass_instance.field1 == 1
        assert dataclass_instance.field2 == "test"

def test_load_from_json_invalid_type():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test.json")
        with open(filepath, "w") as f:
            f.write('{"field1": 1, "field2": "test"}')
        
        with pytest.raises(TypeError):
            load_from_json(filepath, List)  # List is neither a Pydantic model nor a dataclass

def test_union_type_in_hierarchical_configs():
    from typing import Union
    from pydantic import BaseModel, Field

    class ConfigA(BaseModel):
        type: str = "A"
        value_a: int

    class ConfigB(BaseModel):
        type: str = "B"
        value_b: str

    class NestedConfig(BaseModel):
        name: str
        config: Union[ConfigA, ConfigB]

    class RootConfig(BaseModel):
        title: str
        nested_configs: List[NestedConfig]

    # Test data
    test_data = {
        "title": "Test Configuration",
        "nested_configs": [
            {
                "name": "First",
                "config": {"type": "A", "value_a": 42}
            },
            {
                "name": "Second",
                "config": {"type": "B", "value_b": "Hello"}
            }
        ]
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_config.json")
        with open(filepath, "w") as f:
            json.dump(test_data, f)

        # Load the configuration
        loaded_config = load_from_json(filepath, RootConfig)

        # Assertions
        assert isinstance(loaded_config, RootConfig)
        assert loaded_config.title == "Test Configuration"
        assert len(loaded_config.nested_configs) == 2

        first_nested = loaded_config.nested_configs[0]
        assert first_nested.name == "First"
        assert isinstance(first_nested.config, ConfigA)
        assert first_nested.config.type == "A"
        assert first_nested.config.value_a == 42

        second_nested = loaded_config.nested_configs[1]
        assert second_nested.name == "Second"
        assert isinstance(second_nested.config, ConfigB)
        assert second_nested.config.type == "B"
        assert second_nested.config.value_b == "Hello"

def test_unknown_config_class():
    from typing import Union
    from pydantic import BaseModel

    class KnownConfig(BaseModel):
        type: str = "Known"
        value: int

    class UnknownConfig(BaseModel):
        type: str = "Unknown"
        data: str

    class ModelWithConfig(BaseModel):
        name: str
        config: Union[KnownConfig, UnknownConfig]

        def forward(self):
            if isinstance(self.config, KnownConfig):
                return f"Known: {self.config.value}"
            elif isinstance(self.config, UnknownConfig):
                return f"Unknown: {self.config.data}"
            else:
                return "Error: Unknown config type"

    # Test data
    test_data = {
        "name": "Test Model",
        "config": {"type": "Unknown", "data": "Mystery data"}
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_config.json")
        with open(filepath, "w") as f:
            json.dump(test_data, f)

        # Load the configuration
        loaded_model = load_from_json(filepath, ModelWithConfig)

        # Assertions
        assert isinstance(loaded_model, ModelWithConfig)
        assert loaded_model.name == "Test Model"
        assert isinstance(loaded_model.config, UnknownConfig)
        assert loaded_model.config.type == "Unknown"
        assert loaded_model.config.data == "Mystery data"

        # Test forward method
        assert loaded_model.forward() == "Unknown: Mystery data"

def test_right_forward_from_right_model():
    from typing import Union
    from pydantic import BaseModel

    class ConfigA(BaseModel):
        type: str = "A"
        value_a: int

        def forward(self):
            return f"Config A: {self.value_a}"

    class ConfigB(BaseModel):
        type: str = "B"
        value_b: str

        def forward(self):
            return f"Config B: {self.value_b}"

    class ModelWithConfig(BaseModel):
        name: str
        config: Union[ConfigA, ConfigB]

        def forward(self):
            return self.config.forward()

    # Test data for both config types
    test_data_a = {
        "name": "Model A",
        "config": {"type": "A", "value_a": 42}
    }

    test_data_b = {
        "name": "Model B",
        "config": {"type": "B", "value_b": "Hello"}
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test ConfigA
        filepath_a = os.path.join(tmpdir, "test_config_a.json")
        with open(filepath_a, "w") as f:
            json.dump(test_data_a, f)

        loaded_model_a = load_from_json(filepath_a, ModelWithConfig)
        assert isinstance(loaded_model_a, ModelWithConfig)
        assert isinstance(loaded_model_a.config, ConfigA)
        assert loaded_model_a.forward() == "Config A: 42"

        # Test ConfigB
        filepath_b = os.path.join(tmpdir, "test_config_b.json")
        with open(filepath_b, "w") as f:
            json.dump(test_data_b, f)

        loaded_model_b = load_from_json(filepath_b, ModelWithConfig)
        assert isinstance(loaded_model_b, ModelWithConfig)
        assert isinstance(loaded_model_b.config, ConfigB)
        assert loaded_model_b.forward() == "Config B: Hello"
